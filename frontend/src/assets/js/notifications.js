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
    }
}

export default alertas;