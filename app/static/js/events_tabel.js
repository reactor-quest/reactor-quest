$(document).ready(function() {
    var events_table = $('#events_table');

    function fetchData(callBack){
        $.get(url='ajax/get_events', 
            data={}, 
            success=callBack, 
            dataType='json');
    }

    function post_process_stop_request(responce){
        console.log(responce);
    }

    function try_to_stop_event(){
        var event_id = Number($(this).attr('id'));
        $.get('ajax/stop_event', {'event_id': event_id}, post_process_stop_request)
    }

    fetchData(function(events){
        /**
         * event: id, name, source, status(1)
         */
        console.log(events);
        events_table.empty();
        events.forEach(function(event_obj){
            if(event_obj.access){
                events_table.append(`
                    <tr>
                    <td>${event_obj['name']}</td>
                    <td>${event_obj['source']}</td>
                    <td><button id="${event_obj['id']}" class='btn btn-secondary'><i class="fa fa-times" aria-hidden="true"></i></button></td>
                    </tr>
                `);

                // bind delete action
                $(`#events_table #${event_obj['id']}`).on('click', try_to_stop_event);

            } else {
                events_table.append(`
                    <tr>
                        <td>${event_obj['name']}</td>
                        <td>${event_obj['source']}</td>
                        <td></td>
                    </tr>
                `);
            }


        });        
    });



});