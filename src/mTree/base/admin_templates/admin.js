$.(document).ready(function() {
    // Use a "/test" namespace.
    // An application can open a connection on multiple namespaces, and
    // Socket.IO will multiplex all those connections on a single
    // physical channel. If you don't care about multiple channels, you
    // can set the namespace to an empty string.
    namespace = '/admin';
    user_id = '';

    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    //var socket = io.connect('https://' + document.domain + namespace);


    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function() {
        console.log("Admin connected...");
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    socket.on('admin_action', function(msg) {
        console.log(msg);
        switch(msg["action"]){
            case "add_user":
              add_user_to_list(msg);
              break;
            case "update_admin_table":
              update_user_list(msg);
              break;
            case "drop_user":
              add_user_to_inactive_list(msg);
              break;
          };
    });

    function add_user_to_list(msg){
        console.log("Appending another row");
        new_user_record = $('<tr>').attr("id",msg["data"]["user_id"]).append(
          $('<td>').attr("id","user_id").text(msg["data"]["user_id"]),
          $('<td>').attr("id","current").text(msg["data"]["current"]),
          $('<td>').attr("id","join_time").text(msg["data"]["join_time"]),
          $('<td>').attr("id","last_contact").text("-"),
          $('<td>').attr("id","total_earnings").text("-"));
        console.log(new_user_record);

        $("#active_users > tbody:last").append(new_user_record);

    }

    function update_user_list(msg){
        $("#" + msg["data"]["user_id"]).find("#total_earnings").html(msg["data"]["total_earnings"]);
        $("#" + msg["data"]["current"]).find("#last_contact").html(msg["data"]["current"]);
        $("#" + msg["data"]["last_contact"]).find("#last_contact").html(msg["data"]["last_contact"]);

    }


    function add_user_to_inactive_list(msg){
        console.log("Appending another row");
        inactive_user_record = $('<tr>').attr("id",msg["data"]["user_id"]).append(
          $('<td>').attr("id","user_id").text(msg["data"]["user_id"]),
          $('<td>').attr("id","current").text(msg["data"]["current"]),
          $('<td>').attr("id","join_time").text(msg["data"]["join_time"]),
          $('<td>').attr("id","last_contact").text(msg["data"]["last_contact"]),
          $('<td>').attr("id","total_earnings").text("-"));
        console.log(inactive_user_record);
        $("#active_users").find("#" + msg["data"]["user_id"]).remove();

        $("#inactive_users > tbody:last").append(inactive_user_record);

    }

    function update_inactive_user_list(msg){
        $("#" + msg["data"]["user_id"]).find("#total_earnings").html(msg["data"]["total_earnings"]);
        $("#" + msg["data"]["user_id"]).find("#last_contact").html(msg["data"]["last_contact"]);

    }



    // Interval function that tests message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    var ping_pong_times = [];
    var start_time;

    // Handler for the "pong" message. When the pong is received, the
    // time from the ping is stored, and the average of the last 30
    // samples is average and displayed.


    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server in a
    // variety of ways
    $('form#emit').submit(function(event) {
        socket.emit('my_event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
        return false;
    });
    $('form#join').submit(function(event) {
        socket.emit('join', {room: $('#join_room').val()});
        return false;
    });
    $('form#leave').submit(function(event) {
        socket.emit('leave', {room: $('#leave_room').val()});
        return false;
    });
    $('form#send_room').submit(function(event) {
        socket.emit('my_room_event', {room: $('#room_name').val(), data: $('#room_data').val()});
        return false;
    });
    $('form#close').submit(function(event) {
        socket.emit('close_room', {room: $('#close_room').val()});
        return false;
    });
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect_request');
        new_user_record = $('<tr>').attr("id",msg["data"]["user_id"]).append(
          $('<td>').attr("id","user_id").text(msg["data"]["user_id"]),
          $('<td>').attr("id","join_time").text(msg["data"]["join_time"]),
          $('<td>').attr("id","last_contact").text("-"),
          $('<td>').attr("id","total_earnings").text("-"));
        console.log(new_user_record);

        $("#active_users > tbody:last").append(new_user_record);
        return false;
    });
    $('button').click(function(){
            var button_pressed = this.id;
            message = {};
            switch(button_pressed){
            case "start_experiment":
                message['control'] = "START";
                break;
            case "pause_experiment":
                message['control'] = "PAUSE";
                break;
            case "stop_experiment":
                message['control'] = "STOP";
                break;
            }
            socket.emit('admin_control', message);

        }
    );
});