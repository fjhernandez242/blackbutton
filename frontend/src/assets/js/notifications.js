import Swal from "sweetalert2";

const alertas = {
    alertSuccess(mensaje) {
        Swal.fire({
            icon: "success",
            title: mensaje,
            showConfirmButton: false,
            timer: 1500
        });
    },

    alertError(mensaje) {
        Swal.fire({
            icon: "error",
            title: mensaje,
            showConfirmButton: false,
            timer: 1500
        });
    },

    alertWarning(mensaje, btn = true, time = 1500) {
        Swal.fire({
            icon: "warning",
            title: mensaje,
            showConfirmButton: btn,
            timer: time
        });
    },

    alertQuestion(mensaje) {
        return Swal.fire({
            icon: "question",
            title: mensaje,
            showConfirmButton: true,
            showCancelButton: true,
            confirmButtonText: "Si",
            confirmButtonColor: "#B53471",
            denyButtonText: "Cancelar"
        });
    },

    questionTypeSend() {
        return Swal.fire({
            icon: "question",
            title: "Elige el método de envio",
            showConfirmButton: true,
            showCancelButton: true,
            confirmButtonText: "WhatsApp",
            confirmButtonColor: "#075E54",
            cancelButtonText: "SMS",
            cancelButtonColor: "#006AFF"
        });
    }
}

export default alertas;