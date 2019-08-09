import React from 'react';
import PropTypes from 'prop-types';
import withStyles from '@material-ui/core/styles/withStyles';
import Typography from '@material-ui/core/Typography';

const styles = theme => ({
    footer: {
        paddingTop: theme.spacing.unit,
    },
    messageBox: {
        width: '100%',
        textAlign: 'center',
        background: '#ffd966',
        borderRadius: 5,
        marginTop: theme.spacing.unit * 2,
        padding: theme.spacing.unit * .7,
    },
});

const ErrorMessageBoxComponent = ({classes, errorMsg}) => {
    if (!errorMsg) return null;

    return (<div className={classes.messageBox}>
        <Typography variant="subtitle1">
            {errorMsg.message || 'Сталася помилка'}
        </Typography>
    </div>);
};

ErrorMessageBoxComponent.propTypes = {
    classes: PropTypes.object.isRequired,
    errorMsg: PropTypes.any,
};

export const ErrorMessageBox = withStyles(styles)(ErrorMessageBoxComponent);
