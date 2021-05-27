import React, { useState, useEffect, Component } from 'react';
import ReactDOM from "react-dom";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useParams,
  useRouteMatch
} from "react-router-dom";
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import SocketClientComponent from "./SocketClientComponent";
import Typography from '@material-ui/core/Typography';


class SimulationRunner {
  constructor()
  {
      if(!SimulationRunner.instance){
          //this._instance = new StateManager();
          this.mtree_type = null;
          this.name = null;
          this.id = null;
          this.environment = null;
          // Multiple institutions...
          this.institution = null;
          this.agents = [];
          this.properties = {}
          this.agent_ui = null;

          SimulationRunner.instance = this;          
        }
     
        return SimulationRunner.instance;
  }

  readJson(json){
    SimulationRunner.instance.mtree_type = json["mtree_type"];
    SimulationRunner.instance.name = json.name;
    SimulationRunner.instance.id = json["id"];
    SimulationRunner.instance.environment = json["environment"];
    SimulationRunner.instance.institution = json["institution"];
    SimulationRunner.instance.number_of_runs = json["number_of_runs"];
    SimulationRunner.instance.agents = json["agents"];
    SimulationRunner.instance.properties = json["properties"];
    SimulationRunner.instance.agent_ui = json["agent_ui"];
    console.log("STUFF");
    console.log(json["name"]);
    console.log(SimulationRunner.instance.name);
    console.log(json);
  }


}


const useStyles = makeStyles((theme) => ({
    root: {
      flexGrow: 1,
    },
    paper: {
      height: 140,
      width: 100,
    },
    control: {
      padding: theme.spacing(5),
    },
    table: {
        minWidth: 150,
      },
  }));
  

function SimulationRunners() {
    let experiment = new SimulationRunner();
    let { path, url } = useRouteMatch();

    const classes = useStyles();

    const [configurations, setConfigurations] = useState([]);
    const [configuration, setConfiguration] = useState(null);



    useEffect(() => {
        SocketClientComponent.getConfigurations(setConfigurations);
      }, []);

    return (
      <div>
        <Switch>
            <Route exact path={path}>
                <Paper>
                <TableContainer component={Paper}>
                    <Table className={classes.table} aria-label="simple table">
                        <TableHead>
                        <TableRow>
                            <TableCell>Configuration</TableCell>
                            <TableCell>Details</TableCell>
                        </TableRow>
                        </TableHead>
                        <TableBody>
                        {configurations.map((row) => (
                            <TableRow key={row}>
                            <TableCell component="th" scope="row">{row[0]}</TableCell>
                            <TableCell component="th" scope="row"> <Link to={`${url}/${row[0]}`} onClick={() => {
                              SimulationRunner.instance.readJson(JSON.parse(row[1]));
                              SocketClientComponent.runSimulationConfiguration(row[1]);
                              }}>Run Configuration</Link></TableCell>
                            </TableRow>
                        ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                </Paper>
            </Route>
            <Route path={`${path}/:configuration`}>

            <Paper>
            <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Property</TableCell>
            <TableCell align="right">Value</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
            <TableRow >
              <TableCell component="th" scope="row">
                Experiment Type
              </TableCell>
              <TableCell align="right">{SimulationRunner.instance.mtree_type}</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>

            <TableRow >
              <TableCell component="th" scope="row">
                Name
              </TableCell>
              <TableCell align="right">{SimulationRunner.instance.name}</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>

            <TableRow >
              <TableCell component="th" scope="row">
                ID
              </TableCell>
              <TableCell align="right">{SimulationRunner.instance.id}</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>

            <TableRow >
              <TableCell component="th" scope="row">
                Environment
              </TableCell>
              <TableCell align="right">{SimulationRunner.instance.environment}</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>

            <TableRow >
              <TableCell component="th" scope="row">
                Institution
              </TableCell>
              <TableCell align="right">{SimulationRunner.instance.institution}</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>

            <TableRow >
              <TableCell component="th" scope="row">
                Agents
              </TableCell>
              <TableCell align="right">{SimulationRunner.instance.mtree_type}</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>

            <TableRow >
              <TableCell component="th" scope="row">
                Properties
              </TableCell>
              <TableCell align="right">{SimulationRunner.instance.mtree_type}</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>

            <TableRow >
              <TableCell component="th" scope="row">
                Agent UI
              </TableCell>
              <TableCell align="right">{SimulationRunner.instance.agent_ui}</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>

        </TableBody>
      </Table>
    </TableContainer>
              </Paper>

            
            </Route>

      </Switch>
        
      </div>
    );
  };
  

export default SimulationRunners