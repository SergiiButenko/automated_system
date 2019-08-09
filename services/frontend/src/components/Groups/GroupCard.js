import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';

import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

import PageSpinner from '../shared/PageSpinner';
import {webUri} from '../../constants/uri';
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
export default class GroupCard extends React.Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        group: PropTypes.object.isRequired,
        loading: PropTypes.bool.isRequired,
    };

    static contextTypes = {
        router: PropTypes.object
    };

    redirectToGroup = (id) => (e) => {
        this.context.router.history.push(webUri.GROUPS(id));
    };

    redirectToSettings = (id) => (e) => {
        console.log(this.router.history)
    };

    render() {
        const {classes, loading, group} = this.props;

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
                    spacing={24}
                    direction="row"
                    justify="space-between"
                    alignItems="center"
                >
                    <Grid item xs={8} onClick={this.redirectToGroup(group.id)}>
                        <Typography variant="h5" component="h3">
                            {group.name}
                        </Typography>
                        <Typography component="p">
                            {group.description}
                        </Typography>
                    </Grid>
                    <Grid item xs={1} onClick={this.redirectToGroup(group.id)}>
                        <ArrowForwardIos />
                    </Grid>
                    <Grid item xs={1} onClick={this.redirectToSettings(group.id)}>
                        <Settings />
                    </Grid>
                </Grid>
            </Paper>
        );
    }
}
