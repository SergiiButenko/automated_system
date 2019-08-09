import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import {connect} from 'react-redux';
import { withRouter } from 'react-router-dom';


import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { Button } from '@material-ui/core';

import {getDevices} from '../../selectors/devices';
import {fetchDeviceById, postDeviceTasks} from '../../actions/device';
import PageSpinner from '../shared/PageSpinner';
import LoadingFailed from '../shared/LoadingFailed';
import LineCard from '../shared/cards/LineCard';
import DeviceCard from '../shared/cards/DeviceCard';

const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
});

const mapStateToProps = (state) => {
    return getDevices(state);
};
@withStyles(styles)
@withRouter
@connect(mapStateToProps, {fetchDeviceById, postDeviceTasks})
export default class Devices extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        devices: PropTypes.object.isRequired,
        loading: PropTypes.bool.isRequired,
        deviceFetchError: PropTypes.any,
    };

    componentDidMount() {
        this.props.fetchDeviceById(this.props.match.params.deviceId);
    }

    render() {
        const {classes, loading, deviceFetchError, devices, match: {params}, postDeviceTasks} = this.props;
        const device = devices[params.deviceId];
        
        if (loading) {
            return <PageSpinner/>;
        }

        if (deviceFetchError) {
            return <LoadingFailed errorText={deviceFetchError}/>;
        }

        return (
            <>
            <Grid container spacing={24}>
                <Grid item xs={12}>
                    <Paper className={classes.root} elevation={1}>
                        <Grid container spacing={24}>
                            <Grid item xs={8}>
                                <Typography variant="h5" component="h3">
                                    {device.name}
                                </Typography>
                                <Typography component="p">
                                    {device.description}
                                </Typography>
                                <Typography component="p">
                                    <pre>{JSON.stringify(device.settings, null, 2) }</pre>
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Button
                                onClick={() => postDeviceTasks(device.id)}
                                >
                                    Почати полив
                                </Button>
                            </Grid>
                        </Grid>
                    </Paper>
                </Grid>

                {
                    Object.keys(device.lines).map(function (id, index) {
                        return (
                            <Grid item xs={12}>
                                <LineCard lineId={device.lines[id].id} key={device.lines[id].id}/>
                            </Grid>
                        );
                    })
                }

            </Grid>
            </>
        );
    }
}
