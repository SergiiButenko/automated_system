import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';

import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

import PageSpinner from '../PageSpinner';
import {webUri} from '../../../constants/uri';
import ArrowForwardIos from '@material-ui/icons/ArrowForwardIos';
import Settings from '@material-ui/icons/Settings';

const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
});

@withStyles(styles)
export default class DeviceCard extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        device: PropTypes.object.isRequired,
        //loading: PropTypes.bool.isRequired,
    };

    static contextTypes = {
        router: PropTypes.object
    };

    redirectToDevice = (id) => (e) => {
        this.context.router.history.push(webUri.DEVICES(id));
    };

    redirectToSettings = (id) => (e) => {
        console.log(this.context.router.history);
    };

    render() {
        const {classes, loading, device} = this.props;

        if (loading) {
            return <PageSpinner/>;
        }

        return (
            <Paper
                className={classes.root}
                elevation={1}
            >
                <Grid
                    container
                    spacing={16}
                    direction="row"
                    justify="space-between"
                    alignItems="center"
                >
                    <Grid item xs={8} onClick={this.redirectToDevice(device.id)}>
                        <Typography variant="h5" component="h3">
                            {device.name}
                        </Typography>
                        <Typography component="p">
                            {device.description}
                        </Typography>
                        <Typography component="p">
                            {JSON.stringify(device.settings, null, 2)}
                        </Typography>
                    </Grid>
                    <Grid item xs={1} onClick={this.redirectToDevice(device.id)}>
                        <ArrowForwardIos />
                    </Grid>
                </Grid>
            </Paper>
        );
    }
}
