import React from "react";
import Grid from '@material-ui/core/Grid';
import List from '@material-ui/core/List';
import Paper from '@material-ui/core/Paper';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';

import { DropzoneArea } from "material-ui-dropzone";
import { withStyles } from "@material-ui/core/styles";

import Frame from "./components/Frame";

const useStyles = theme => ({
    root: {
        margin: "20px",
        display: 'flex',
        flexWrap: "wrap",
        justifyContent: 'space-around',
    },
    item: {
        margin: "20px"
    },
    dropzone: {
        margin: "20px",
        width: "600px",
        height: "auto"
    },
    list: {
        flexWrap: 'nowrap',
        height: "auto",
        overflowY: "auto"
    }
});

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            files: [],
            modal: false
        };
    }
    
    onFileDrop(files) {
        this.setState({ files: files });
    }
    
    render() {
        const { classes } = this.props;
        return (
            <Grid className={classes.root} container direction="column" justify="center" alignItems="center" style={{wrap:"nowrap"}}>
                <Grid item>
                    <DropzoneArea dropzoneClass={classes.dropzone} acceptedFiles={['image/jpeg', 'image/png']} onChange={this.onFileDrop.bind(this)}/>
                </Grid>
                <Grid item>
                    <GridList className={classes.list} component={Paper} spacing={15} cols={2.5}>
                        <GridListTile><Frame frame={10} /></GridListTile>
                        <GridListTile><Frame frame={11} /></GridListTile>
                        <GridListTile><Frame frame={12} /></GridListTile>
                        <GridListTile><Frame frame={13} /></GridListTile>
                        <GridListTile><Frame frame={14} /></GridListTile>
                        <GridListTile><Frame frame={15} /></GridListTile>
                        <GridListTile><Frame frame={16} /></GridListTile>
                    </GridList>
                </Grid>
            </Grid>
        );
    }
}


export default withStyles(useStyles)(App);
