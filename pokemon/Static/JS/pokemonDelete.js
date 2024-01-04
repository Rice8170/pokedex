window.addEventListener('load',function(){
    form = document.getElementById('formDelete');
    form.addEventListener('submit', event =>{
        event.preventDefault();
        console.log(event)
        Swal.fire({
            title: "Eliminar pokemon",
            text: "Perderasa tu poquemon. ¿Estas Seguro?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Eliminar'
        }).then((result) => {
            if(result.isConfirmed){
                form.submit();
            }
        })
    })
})
