window.addEventListener('load',function(){

})

const preDelete = function(pokemonId){
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
            location.href =`http://127.0.0.1:8000/pokemon/delete/${pokemonId}`;
        }
    })
}