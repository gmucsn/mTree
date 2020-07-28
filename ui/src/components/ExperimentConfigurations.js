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
  

function ExperimentConfigurations() {

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
                            <TableCell component="th" scope="row"> <Link to={`${url}/${row[0]}`} onClick={() => {setConfiguration(row[1])}}>Details</Link></TableCell>
                            </TableRow>
                        ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                </Paper>
            </Route>
            <Route path={`${path}/:configuration`}>
            <Paper>{configuration}</Paper>
            </Route>
      </Switch>
        
      </div>
    );
  };
  

export default ExperimentConfigurations