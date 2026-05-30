var user_id = "";
var socket = "";

    /*
     * This function makes a call back to the server to post a
     * dictionary on the board. It is used both for requested (tag=peek)
     * and automatic (tag=click, tag=key) dictionaries. It decorates the
     * dictionary with two additional entries that indicate (i) client
     * number and (ii) a time stamp; these are used in all dictionaries
     * posted by the client, so we might as well just code them once.
     */


     (function($) {
        $.QueryString = (function(a) {
            if (a == "") return {};
            var b = {};
            for (var i = 0; i < a.length; ++i)
            {
                var p=a[i].split('=', 2);
                if (p.length != 2) continue;
                b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
            }
            return b;
        })(window.location.search.substr(1).split('&'))
    })(jQuery);

    function put(obj){
      /*
       * Keep in mind that client is a string and we want an integer
       * here, so subtract 0.
       */


      //obj.client = client - 0;
      //obj.time = (new Date()).getTime();
      obj.user_id = user_id;

        alert("SHOULD BE SENDING SOMETHING...");

      socket.emit('put', {data: JSON.stringify(obj)});

    }

    function add(item, msg){
        var new_div = $("<div id='" + msg["new_div_id"] + "'></div>");
        new_div.append(item);

        switch(msg["add_instruction"]) {
            case "append":
                $(document.body).append(new_div);
                break;
            case "prepend":
                $(document.body).prepend(new_div);
                break;
            case "insert":
                // special case
                $("#" + msg["new_div_id"]).html(item);
                break;

            }

         decorate($("#" + msg["new_div_id"]));

        //TODO flag for append/prepend
    }

    function del_content(item, msg){
        var target_div = msg["div_id"];
        $("#" + target_div).empty();
    }

    function pause_screen_control(data, msg){
        console.log("Attempting to pause things: " + msg["experiment_state"]);
        switch(msg["experiment_state"]){
            case "paused":
                $("#cover").show(); // brings up the pause screen
                break;
            case "running":
               $("#cover").hide(); // brings up the pause screen
               break;
        }
    }

    function decorate(elt) {
      /*
       * Key presses that happen when a text field is in focus
       * should be processed the normal way and should not result in
       * events being reported to the server.
       */
      var text_fields = elt.find("input:text,textarea");
      text_fields.keypress(function(e) {
        e.stopPropagation();
      });

      /*
       * When somebody clicks a button, or a "clickable" element, we
       * catch the click and report it.
       */
       if (elt.is(":submit")){
            elt.unbind("click");
            elt.click(function (e) {
                put({ "tag": "click",  "id": e.currentTarget.id});
        });
       }

      var buttons = elt.find(":submit,:button,.clickable");
        buttons.unbind("click");
        buttons.click(function (e) {
            message_hash = {"tag": "click",  "id": e.currentTarget.id};

            console.log("BUTTON BEING PRESSED");
            if ($(e.currentTarget).data()){
                console.log("BUTTON HAS ADDITIONAL DATA");

                if (typeof $(e.currentTarget).data("associatedFields") !== 'undefined'){
                    associatedFields = $(e.currentTarget).data("associatedFields").split(" ");
                    associatedFields.forEach(function(entry) {
                       message_hash[entry] = $("#" + entry).val();
                    });
                }

                if (typeof $(e.currentTarget).data("answer") !== 'undefined'){
                    message_hash["answer"] = $(e.currentTarget).data("answer");
                }

                if (typeof $(e.currentTarget).data("controllerAction") !== 'undefined'){
                    console.log("Preparing button for controller link");
                    message_hash["controllerAction"] = $(e.currentTarget).data("controllerAction");
                }
            }

            if (!$(e.currentTarget).hasClass("dropdown-toggle")){
                put(message_hash);
            }
        });

      /*
       * When an element is marked with class "bait", we want to
       * turn on class "mouse" whenever the mouse is over it. (This
       * is for implementing "hover" effects.)
       */
      var mousetraps = elt.find(".bait");
      mousetraps.unbind("mouseenter");
      mousetraps.unbind("mouseleave");
      mousetraps.bind("mouseenter mouseleave", function(e) {
        $(e.target).closest(".bait").toggleClass("mouse");
      });
    }

// Core initialization for socket connections
$(document).ready(function() {
    // Use a "/test" namespace.
    // An application can open a connection on multiple namespaces, and
    // Socket.IO will multiplex all those connections on a single
    // physical channel. If you don't care about multiple channels, you
    // can set the namespace to an empty string.
    namespace = '/subject';

    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    //socket = io.connect('https://' + document.domain + namespace);
    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function() {
        //alert("CONNECTED");
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    socket.on('my_response', function(msg) {
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    });

    // Interval function that tests message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    var ping_pong_times = [];
    var start_time;


    function willow_command(action, data, msg){
        console.log("Action Happening: " + action + " for div: " + data);
        switch(action) {
        case "show":
            decorate($("#" + data));
            $("#" + data).show();
            break;
        case "hide":
            decorate($("#" + data));
            $("#" + data).hide();
            break;
        case "let":
            //alert(data);
            decorate($("#" + data).html(msg["content"]));
            break;
        case "set":
            $("#" + data).attr(msg["property_name"], msg["property_value"]);
            break;
        case "add":
            add(data, msg);
            break;
        case "del_content":
            del_content(data, msg);
            break;
        case "set_user_id":
            // Should check to see if already set...
            user_id = data;
            $("#user_id_text").html(user_id)
            break;
        case "get_parameter":
            querystring = $.QueryString[data]
            return querystring;
            break;
        case "pause":
            pause_screen_control(data, msg);
            break;



        }
    }


    // Handler code for receiving willow specific commands
    socket.on('willow_action', function(msg) {
       //alert("MESSAGE RECEIVED");

        action = msg.data["action"];
        item = msg.data["item"];
        console.log(action + item + msg.data);
        willow_command(action, item, msg.data);  // Reconsider this TODO

    });

    socket.on('willow_action_response', function (msg, fn) {
        console.log(name);
        action = msg.data["action"];
        item = msg.data["item"];
        response = willow_command(action, item, msg.data);  // Reconsider this TODO
        fn(response);
    });


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
        return false;
    });
});