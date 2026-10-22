const csrfToken = document.querySelector(
    "[name=csrfmiddlewaretoken]"
).value;
async function apiRequest(url, options = {}) {

    let response;

    try {
        response = await fetch(url, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                ...(options.headers || {})
            },
            credentials: "same-origin"
        });
    } catch {
        throw new Error(
            "Сервис временно недоступен. Попробуйте позже."
        );
    }

    if (response.status >= 500) {
        throw new Error(
            "Сервис временно недоступен. Попробуйте позже."
        );
    }

    let data = null;
    if (response.status !== 204) {
        data = await response.json().catch(() => null);
    }
    if (!response.ok) {
      const errorText =
        data && typeof data === "object"
            ? Object.values(data).flat().join(" ")
            : typeof data === "string"
                ? data
                : "Ошибка выполнения запроса";

      throw new Error(errorText);
}
    return data;
}


const categorySelect =
    document.getElementById("category");
const form =
    document.getElementById("ticket-form");
const titleInput =
    document.getElementById("title");
const message =
    document.getElementById("message");
function showMessage(text, isError = false) {
    message.textContent = text;
    message.className =
        "alert " + (isError ? "alert-danger" : "alert-success");
}
async function loadCategories() {
    const categories = await apiRequest(
        "/api/categories/"
    );
    categorySelect.replaceChildren();
    for (const category of categories) {
        const option = document.createElement("option");
        option.value = category.id;
        option.textContent = category.name;
        categorySelect.append(option);
    }
}
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
        await apiRequest("/api/tickets/", {
            method: "POST",
            body: JSON.stringify({
                title: titleInput.value,
                category: Number(categorySelect.value)
            })
        });
        titleInput.value = "";
        showMessage("Заявка успешно создана");
        await loadTickets();
    } catch (error) {
        showMessage(
            "Не удалось создать заявку: " + error.message,
            true
        );
    }
});


const list = document.getElementById("tickets-list");
const loading = document.getElementById("loading");
const filter = document.getElementById("status-filter");
const searchInput = document.getElementById("ticket-search");
const totalCount = document.getElementById("total-count");
const doneCount = document.getElementById("done-count");
async function loadTickets() {
    loading.hidden = false;
    const params = new URLSearchParams();
    if (filter.value) {
        params.set("status", filter.value);
    }
    const query = params.toString();
    const url = "/api/tickets/" + (query ? "?" + query : "");
    try {
        const allTickets = await apiRequest("/api/tickets/");
        totalCount.textContent = allTickets.length;
        doneCount.textContent = allTickets.filter(
            ticket => ticket.status === "done"
        ).length;
        const tickets = filter.value
            ? await apiRequest(url)
            : allTickets;
        const searchText = searchInput.value.trim().toLowerCase();
        const visibleTickets = tickets.filter(ticket =>
            ticket.title.toLowerCase().includes(searchText) ||
            ticket.category_name.toLowerCase().includes(searchText)
        );
        list.replaceChildren();
        if (visibleTickets.length === 0) {
            const empty = document.createElement("p");
            empty.textContent = "Заявки не найдены";
            list.append(empty);
            return;
        }

    for (const ticket of visibleTickets) {
      const row = document.createElement("div");
      row.className = "ticket-row border-bottom py-3";
      const title = document.createElement("div");
      title.textContent =
        ticket.title + " — " + ticket.category_name;
      const status = document.createElement("span");
      status.className = "badge bg-blue-lt";
      const statusNames = {
        new: "Новая",
        progress: "В работе",
        done: "Выполнена"
      };
      status.textContent = statusNames[ticket.status];
      const actions = document.createElement("div");
      actions.className = "ticket-actions";
      const statusSelect = document.createElement("select");
      statusSelect.className = "form-select form-select-sm";
      const placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = "Выберите статус";
      statusSelect.append(placeholder);
      const nextStatuses = {
        new: { value: "progress", text: "В работе" },
        progress: { value: "done", text: "Выполнена" }
      };
      const next = nextStatuses[ticket.status];
      if (next) {
        const option = document.createElement("option");
        option.value = next.value;
        option.textContent = next.text;
        statusSelect.append(option);
      } else {
        statusSelect.disabled = true;
        placeholder.textContent = "Завершена";
      }
      const changeButton = document.createElement("button");
      changeButton.className = "btn btn-primary btn-sm";
      changeButton.textContent = "Изменить статус";
      changeButton.disabled = !next;
      changeButton.addEventListener("click", () => {
        if (!statusSelect.value) {
            showMessage("Сначала выберите статус", true);
            return;
        }
        changeStatus(ticket.id, statusSelect.value);
      });
      const deleteButton = document.createElement("button");
      deleteButton.className = "btn btn-danger btn-sm";
      deleteButton.textContent = "Удалить";
      deleteButton.addEventListener("click", () => {
        deleteTicket(ticket.id, ticket.title);
      });
      actions.append(statusSelect, changeButton, deleteButton);
      row.append(title, status, actions);
      list.append(row);
}
    } catch (error) {
        showMessage(
            "Не удалось загрузить заявки: " + error.message,
            true
        );
    } finally {
        loading.hidden = true;
    }
}
filter.addEventListener("change", loadTickets);
searchInput.addEventListener("input", loadTickets);
document.getElementById("show-all").addEventListener("click", () => {
    filter.value = "";
    const search = document.getElementById("ticket-search");
    if (search) search.value = "";
    loadTickets();
});
document.getElementById("show-done").addEventListener("click", () => {
    filter.value = "done";
    const search = document.getElementById("ticket-search");
    if (search) search.value = "";
    loadTickets();
});
let searchTimer;
searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadTickets, 250);
});
async function initialize() {
    try {
        await loadCategories();
        await loadTickets();
    } catch (error) {
        showMessage(
            "Ошибка инициализации: " + error.message,
            true
        );
    }
}
initialize();


async function changeStatus(ticketId, newStatus) {
    try {
        await apiRequest(`/api/tickets/${ticketId}/`, {
            method: "PATCH",
            body: JSON.stringify({
                status: newStatus
            })
        });
        await loadTickets();
        showMessage("Статус заявки успешно изменён");
    } catch (error) {
        showMessage(
            "Не удалось изменить статус: " + error.message,
            true
        );
    }
}
async function deleteTicket(ticketId, ticketTitle) {
    const confirmed = confirm(
        `Удалить заявку «${ticketTitle}»?`
    );
    if (!confirmed) {
        return;
    }
    try {
        await apiRequest(`/api/tickets/${ticketId}/`, {
            method: "DELETE"
        });
        await loadTickets();
        showMessage("Заявка успешно удалена");
    } catch (error) {
        showMessage(
            "Не удалось удалить заявку: " + error.message,
            true
        );
    }
}
