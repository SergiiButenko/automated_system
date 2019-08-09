import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';

const styles = theme => ({
    progress: {
        margin: `${theme.spacing.unit * 2} auto`,
    },
    wrapper: {
        width: '100%',
    },
});

function PageSpinner(props) {
    const { classes } = props;
    return (
        <div className={classes.wrapper}>
            <CircularProgress className={classes.progress} />
        </div>
    );
}

PageSpinner.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(PageSpinner);