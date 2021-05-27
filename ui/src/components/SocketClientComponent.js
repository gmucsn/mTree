import React, { useEffect, useState } from "react";
import io from "socket.io-client";
const ENDPOINT = "http://127.0.0.1:5000/admin";

// export default function SocketClientComponent() {
//   const [response, setResponse] = useState("");

//   useEffect(() => {
//     const socket = socketIOClient(ENDPOINT);
//     console.log("CONNECTING")
//     socket.on("FromAPI", data => {
//       setResponse(data);
//     });

//   }, []);

//   return (
//     <p>
//       It's <time dateTime={response}>{response}</time>
//     </p>
//   );
// }



class SocketClientComponent {
    constructor(){
        this.agents = null;
        this.institutions = null;
        this.environments = null;

      this.socket = io.connect(ENDPOINT);

      this.socket.on('chat', (data) => {console.log("RECIEVED A MESSAGAE");
            this.processMessage(data);
        });

        this.socket.on('response', (data) => {
            console.log("RECIEVED A MESSAGAE");
            this.processMessage(data);
        });

      this._data = [];
      console.log("STUFF here too");
    }

    componentRegister(agents, institutions, environments){
        this.agents = agents;
        this.institutions = institutions;
        this.environments = environments;
    }

    processMessage(message){
        console.log("****************");
        console.log(message);
        console.log("^^^^^^^^^^^^^^^^^^^^^^^");
        if (message["message"] == "component_list"){
            this.agents(message["data"]["agents"]);
            this.institutions(message["data"]["institutions"]);
            this.environments(message["data"]["environments"]);
            console.log(this.agents);
        } else if (message["message"] == "subject_pool_data"){
            this.subjectPoolIDs(message["data"]["subject_ids"]);
            this.subjectPool(message["data"]["subject_hash"]);
            console.log("Should have set subject pool info");
        } else if (message["message"] == "configuration_data"){
            this.configurations(message["data"]);
            console.log("Should have set subject pool info");
        } else {
            console.log("SOME OTHER MESSAGE");
        }
    }

    sendMessage(){

        this.socket.emit("message", "HUOPPLA");
    }

    getComponentList(agents, institutions, environments){
        this.agents = agents;
        this.institutions = institutions;
        this.environments = environments;
        this.socket.emit("get_components", "");
    }

    runSimulationConfiguration(configuration_name){
        this.configurations = {"configuration": configuration_name};
        this.socket.emit("run_simulation_configuration", this.configurations);
        console.log("should be getting configurations")
    }

    getSubjectPool(subjectPoolIDs, subjectPool){
        this.subjectPoolIDs = subjectPoolIDs;
        this.subjectPool = subjectPool;
        this.socket.emit("get_subject_pool", "");
        console.log("should be getting subjec tpool")
    }

    getConfigurations(configurations){
        this.configurations = configurations;
        this.socket.emit("get_configurations", "");
        console.log("should be getting configurations")
    }


    echo(){
        console.log("SECHODSFLKAHJ");
    }
}
  
  const instance = new SocketClientComponent();
  //Object.freeze(instance);
  
  export default instance;
  