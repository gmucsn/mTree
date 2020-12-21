import React, { useState, useEffect, Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import Badge from '@material-ui/core/Badge';
import Container from '@material-ui/core/Container';
import { Link } from "react-router-dom";
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import NotificationsIcon from '@material-ui/icons/Notifications';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/Dashboard';
import PeopleIcon from '@material-ui/icons/People';
import AssignmentIcon from '@material-ui/icons/Assignment';
import SocketClientComponent from "./components/SocketClientComponent";
import Home from './components/Home';
import SubjectPool from './components/SubjectPool';
import ComponentList from './components/ComponentList';
import LayersIcon from '@material-ui/icons/Layers';
import ExperimentConfigurations from './components/ExperimentConfigurations';
import SimulationRunner from './components/SimulationRunner';
import PlayCircleOutlineIcon from '@material-ui/icons/PlayCircleOutline';
import RemoveRedEyeIcon from '@material-ui/icons/RemoveRedEye';

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      <Link color="inherit" href="https://github.com/gmucsn/mtree">
        mTree - Computational Economics Resarch
      </Link>
    </Typography>
  );
}

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24, // keep right padding when drawer closed
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing(7),
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(9),
    },
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'auto',
  },
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  },
  fixedHeight: {
    height: 240,
  },
}));

export default function App() {
  useEffect(() => {
    console.log("STARTING SOMETHING HERE");
    SocketClientComponent.echo();
    SocketClientComponent.sendMessage();
    // Some initialization logic here
  }, []);



  const classes = useStyles();
  const [loadClient, setLoadClient] = useState(true);
  const [open, setOpen] = React.useState(true);
  const handleDrawerOpen = () => {
    setOpen(true);
  };
  const handleDrawerClose = () => {
    setOpen(false);
  };
  const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);


  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar position="absolute" className={clsx(classes.appBar, open && classes.appBarShift)}>
        <Toolbar className={classes.toolbar}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            className={clsx(classes.menuButton, open && classes.menuButtonHidden)}
          >
            <MenuIcon />
          </IconButton>
          <Typography component="h1" variant="h6" color="inherit" noWrap className={classes.title}>
            mTree Admin
          </Typography>
          <IconButton color="inherit">
            <Badge badgeContent={4} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        classes={{
          paper: clsx(classes.drawerPaper, !open && classes.drawerPaperClose),
        }}
        open={open}
      >
        <div className={classes.toolbarIcon}>
          <IconButton onClick={handleDrawerClose}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <div>
      <List>
        <ListItem button component={Link} to="/">
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Home" />
        </ListItem>

        <ListItem button component={Link} to="/component_list">
          <ListItemIcon>
            <LayersIcon />
          </ListItemIcon>
          <ListItemText primary="MES Components" />
        </ListItem>

        <ListItem button component={Link} to="/experiment_configurations">
          <ListItemIcon>
            <AssignmentIcon />
          </ListItemIcon>
          <ListItemText primary="Experimentsf Configurations" />
        </ListItem>

        


        <ListItem button component={Link} to="/subject_pool">
          <ListItemIcon>
          <PeopleIcon />
          </ListItemIcon>
          <ListItemText primary="Subject Pool" />
        </ListItem>
        

        <ListItem button component={Link} to="/run_subject_experiment">
          <ListItemIcon>
          <PlayCircleOutlineIcon />
          </ListItemIcon>
          <ListItemText primary="Run Subject Experiment" />
        </ListItem>

        <ListItem button component={Link} to="/run_simulation">
          <ListItemIcon>
          <RemoveRedEyeIcon />
          </ListItemIcon>
          <ListItemText primary="Run Simulation" />
        </ListItem>

        </List>

  </div>
        
      </Drawer>
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <Container maxWidth="lg" className={classes.container}>
          <Switch>
              <Route path="/" component={Home} exact />
              <Route path="/subject_pool" component={SubjectPool}  />
              <Route path="/component_list" component={ComponentList}  />
              <Route path="/experiment_configurations" component={ExperimentConfigurations}  />
              <Route path="/run_subject_experiment" component={ExperimentConfigurations}  />
              <Route path="/run_simulation" component={SimulationRunner}  />
          </Switch>
        </Container>
      </main>
    </div>
  );
}
