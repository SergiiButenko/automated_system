import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';

import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

import PageSpinner from '../PageSpinner';
import ArrowForwardIos from '@material-ui/icons/ArrowForwardIos';
import Settings from '@material-ui/icons/Settings';
import Battery20 from '@material-ui/icons/Battery20';
import Battery60 from '@material-ui/icons/Battery60';
import Battery90 from '@material-ui/icons/Battery90';
import {getDevices} from '../../../selectors/devices';
import connect from 'react-redux/es/connect/connect';
import {fetchDeviceById, toggleLine} from '../../../actions/device';
import {withRouter} from 'react-router-dom';
import classNames from 'classnames';


const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
    selected: {
        boxShadow: '0 0 0 3px #8dbdf7',
        background: '#dae7f7',
    },
});

const mapStateToProps = (state) => {
    return getDevices(state);
};
@connect(mapStateToProps, {toggleLine})
@withRouter
@withStyles(styles)
export default class LineCard extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        devices: PropTypes.object.isRequired,
        lineId: PropTypes.string.isRequired,
        loading: PropTypes.bool.isRequired,
    };

    static contextTypes = {
        router: PropTypes.object
    };

    render() {
        const {match: {params}, lineId, devices, classes, loading, toggleLine} = this.props;
        const {deviceId} = params;
        const line = devices[deviceId].lines[lineId];
        
        if (loading) {
            return <PageSpinner/>;
        }

        line.selected = !!line.selected || false;
        return (
            <Paper
                className={classNames(classes.root, line.selected && classes.selected)}
                elevation={1}
                onClick={() => toggleLine(deviceId, lineId)}
            >
                <Grid
                    container
                    spacing={24}
                    direction="row"
                    justify="space-between"
                    alignItems="center"
                >
                    <Grid item xs={6}>
                        <Typography variant="h5" component="h3">
                            {line.name}
                        </Typography>
                        <Typography component="p">
                            {line.description + " " + line.selected}
                        </Typography>
                        <Typography component="p">
                            {JSON.stringify(line.settings, null, 2)}
                        </Typography>
                    </Grid>
                    <Grid item>
                        <Battery20 />
                        <Battery60 />
                        <Battery90 />
                    </Grid>
                </Grid>
            </Paper>
        );
    }
}
