$(document).ready(function () {
    const $deletedataelem = $("#deletedata")
    // host
    const host = window.location.origin;
    const access_token = sessionStorage.getItem("access_token")
    if (!access_token) {
        window.localStorage.href = "/home/login/"
    }

    $deletedataelem.click(function (e) {
        e.preventDefault();
        showToast("Starting data deletion process...")
        deleteDataAPICall()

    });


    function deleteDataAPICall() {
        $.ajax({
            url: `${host}/api/v1/tables/sync/delete/`,
            type: 'POST',
            contentType: 'application/json',
            headers: { "Authorization": `Bearer ${access_token}` }, // Set the content type
            success: function (data, status, xhr) {
                if (xhr.status >= 200 && xhr.status <= 205) {
                    showToast("Data deleted successfully...")
                    showToast("Check log in show details...")
                }
                console.log("data", data, status)
                res = data
            },
            error: function (xhr, status, error) {
                if (xhr.status == 401) {
                    window.location.href = '/home/'
                }

                showToast("Error deleting the data..", type = "error")
                showToast("Check logs for more details..", type = "error")

            }
        });
    };

    function showToast(msg, type = null) {
        // const now = new Date();
        // const seconds = now.getSeconds();
        let className = null;
        if (type === "error") {
            className = "bg-danger text-white"; // Red background for error messages
        } else if (type === "success") {
            className = "bg-success text-white"; // Green background for success messages
        } else if (type === "info") {
            className = "bg-info text-white"; // Blue background for info messages
        } else if (type === "warning") {
            className = "bg-warning text-dark"; // Yellow background for warning messages
        }
        let toastElement = $('<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">' +
            '<div class="toast-header">' +
            '<strong class="me-auto">Notification</strong>' +
            '<small class="text-body-secondary">just now</small>' +
            '<button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>' +
            '</div>' +
            '<div class="toast-body">' + msg + '</div>' +
            '</div>');

        $(".toast-container").append(toastElement);
        
        if (className) {
            toastElement.addClass(className);
        }
        // Create a new Toast instance for this specific toast
        let toast = new bootstrap.Toast(toastElement[0]);
        // Show the toast
        toast.show();

        // Optional: You can remove the toast from the DOM after it dismisses
        toastElement.on('hidden.bs.toast', function () {
            toastElement.remove();
        });
    }

});