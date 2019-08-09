import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import {connect} from 'react-redux';
import { withRouter } from 'react-router-dom';

import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { Button } from '@material-ui/core';

import {getGroups} from '../../selectors/groups';
import {fetchGroupById} from '../../actions/group';
import PageSpinner from '../shared/PageSpinner';
import LoadingFailed from '../shared/LoadingFailed';
import {webUri} from '../../constants/uri';
import Link from 'react-router-dom/Link';
import DeviceCard from '../shared/cards/DeviceCard';
import GroupHeader from './GroupHeader';


const styles = theme => ({
    root: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
        width: '100%',
    },
});

const mapStateToProps = (state) => {
    return getGroups(state);
};
@withStyles(styles)
@withRouter
@connect(mapStateToProps, {fetchGroupById})
export default class Group extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        groups: PropTypes.object.isRequired,
        loading: PropTypes.bool.isRequired,
        groupFetchError: PropTypes.any,
    };

    componentDidMount() {
        this.props.fetchGroupById(this.props.match.params.groupId);
    }

    render() {
        const {classes, loading, groupFetchError, groups, match: {params}} = this.props;
        const group = groups[params.groupId];

        if (loading) {
            return <PageSpinner/>;
        }

        if (groupFetchError) {
            return <LoadingFailed errorText={groupFetchError}/>;
        }

        return (
            <>
            <Grid container spacing={24}>
                <Grid item xs={12}>
                    <GroupHeader group={group} key={group.id}/>
                </Grid>
                {group.devices.map((device, i) => {
                    return (
                        <Grid item xs={12}>
                            <DeviceCard device={device} key={device.id}/>
                        </Grid>
                    );
                })}
            
            </Grid>
            </>
        );
    }
}
