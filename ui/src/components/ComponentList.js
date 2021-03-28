import React, { useState, useEffect, Component } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import Link from '@material-ui/core/Link';
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
  

function ComponentList() {
    const classes = useStyles();

    const [agents, setAgents] = useState([]);
    const [institutions, setInstitutions] = useState([]);
    const [environments, setEnvironments] = useState([]);

    useEffect(() => {
        console.log("STARTING SOMETHING HERE");
        SocketClientComponent.getComponentList(setAgents, setInstitutions, setEnvironments);
        //SocketClientComponent.getComponentList();
        // Some initialization logic here
      }, []);
    


    return (
      <div>
<Grid
  container
  direction="row"
  justify="center"
  alignItems="center"
  spacing="2"
>
            <Grid key="agents" item>
            <TableContainer component={Paper}>
                <Table className={classes.table} aria-label="simple table">
                    <TableHead>
                    <TableRow>
                        <TableCell>Agents</TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                    {agents.map((row) => (
                        <TableRow key={row}>
                        <TableCell component="th" scope="row">
                            {row}
                        </TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
                </TableContainer>
            </Grid>
            <Grid key="institutions" item>
            <TableContainer component={Paper}>
                <Table className={classes.table} aria-label="simple table">
                    <TableHead>
                    <TableRow>
                        <TableCell>Institutions</TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                    {institutions.map((row) => (
                        <TableRow key={row}>
                        <TableCell component="th" scope="row">
                            {row}
                        </TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
                </TableContainer>
            </Grid>

            <Grid key="environments" item>
            <TableContainer component={Paper}>
                <Table className={classes.table} aria-label="simple table">
                    <TableHead>
                    <TableRow>
                        <TableCell>Environments</TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                    {environments.map((row) => (
                        <TableRow key={row}>
                        <TableCell component="th" scope="row">
                            {row}
                        </TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
                </TableContainer>
            </Grid>

    </Grid>
      </div>
    );
  };
  

export default ComponentList