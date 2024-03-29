function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let tabPokemons
let categoriesOptions
let colorOption
$('#selCategories').on('input', function (event) {
    
    categoriesOptions = [...event.target.selectedOptions].map(option => option.value)

    tabPokemons.draw()

    
});

$('#selColors').on('input', function (event) {
    
    colorOption = event.target.value
    tabPokemons.draw()
});

$(document).ready(function () {
  
    tabPokemons = $('#tabPokemonList').DataTable({
        lengthMenu: [5,10,20,50,-1],
        columnDefs:[
            {orderable:false, targets:6},
            
        ],
        language: {
            processing:     "Traitement en cours...",
            search:         "Buscar&nbsp;:",
            lengthMenu:     "Mostrando _MENU_ registros",
            info:           "Mostrando de  _START_ a _END_ de _TOTAL_ registros",
            infoEmpty:      "No hay registros",
            infoFiltered:   "(filtrado de un total de _MAX_ registros)",
            loadingRecords: "Chargement en cours...",
            zeroRecords:    "No hay coincidencias",
            emptyTable:     "No hay registros para mostrar",
            paginate: {
                first:      "Primero",
                previous:   "Anterior",
                next:       "Siguente",
                last:       "Último"
            }
        },
        serverSide: true,
        paging: true,
        ajax: {
            url: 'http://127.0.0.1:8000/pokemon/get/',
            type: 'post',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            data: function(d){
                d.categories = categoriesOptions
                d.color = colorOption                
            }
        },
        columns:[
            {data:'name'},
            {data:'category'},
            {data:'weight'},
            {data:'height'},
            {data:'color'},
            {data:'dateCapture'},
            {
                data:'',
                render: function(data, type, row){
                    
                    return `
                        <a  href="../deteail/${row.id}" class="btn btn-outline-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                            </svg>
                            Detalles
                        </a>
                    `
                }
            
            },
        ]
    });
});


