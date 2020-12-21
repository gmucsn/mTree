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
  

function SubjectPool() {

    const classes = useStyles();

    const [subjectPoolIDs, setSubjectPoolIDs] = useState([]);
    const [subjectPool, setSubjectPool] = useState({});
    

    useEffect(() => {
        SocketClientComponent.getSubjectPool(setSubjectPoolIDs, setSubjectPool);
      }, []);

    return (
      <div>
        <Paper>
            <TableContainer component={Paper}>
                <Table className={classes.table} aria-label="simple table">
                    <TableHead>
                    <TableRow>
                        <TableCell>Socket ID</TableCell>
                        <TableCell>Connection Time</TableCell>
                        <TableCell>Last Activity</TableCell>
                        <TableCell>Current State</TableCell>
                        <TableCell>Details</TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                    {subjectPoolIDs.map((row) => (
                        <TableRow key={row}>
                        <TableCell component="th" scope="row">{row}</TableCell>
                        <TableCell component="th" scope="row">Connection Time</TableCell>
                        <TableCell component="th" scope="row">Last Activity</TableCell>
                        <TableCell component="th" scope="row">Current State</TableCell>
                        <TableCell component="th" scope="row"><Link to={`${row[0]}`} onClick={() => {
                              console.log("STUFF");
                              }}>Details</Link></TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
            </TableContainer>


        </Paper>
      </div>
    );
  };
  

export default SubjectPool