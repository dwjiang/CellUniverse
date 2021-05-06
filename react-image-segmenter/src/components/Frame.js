import React from "react";
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';

const testImage = "https://i.imgur.com/a4rRHTc.png";

const useStyles = theme => ({
    root: {
        width: "300px",
        height: "300px",
        margin: "20px"
    },
    header: {
        textAlign: "center"
    },
    media: {
        padding: "8px",
        width: "50%"
    },
    image: {
        width: "100%",
        height: "auto"
    }
});

class Frame extends React.Component {
    constructor(props) {
        super(props);
    }
    
    processImage() {
        
    }
    
    render() {
        const { classes } = this.props;
        return (
            <Card className={classes.root} variant="outlined">
                <CardHeader className={classes.header} title={"Frame " + this.props.frame}/>
                <Grid container direction="column" justify="center" alignItems="center">
                    <Grid item className={classes.media}><CardMedia className={classes.image} component="img" src={testImage}/></Grid>
                    <Grid item className={classes.media}><CardMedia className={classes.image} component="img" src={testImage}/></Grid>
                </Grid>
                <CardContent>

                </CardContent>
            </Card>
        );
    }
}


export default withStyles(useStyles)(Frame);
