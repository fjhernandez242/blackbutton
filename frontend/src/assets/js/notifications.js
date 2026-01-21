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

    alertWarning(mensaje) {
        Swal.fire({
            icon: 'warning',
            title: mensaje,
            showConfirmButton: true,
            timer: 1500
        });
    }
}

export default alertas;