import React, {Component} from 'react';
import Typography from '@material-ui/core/Typography';

import {withStyles} from '@material-ui/core/styles';
import ContactSupport from './ContactSupport';
import PropTypes from 'prop-types';

const styles = {
    errorLabel: {
        textAlign: 'center',
        width: '100%',
    },
};

@withStyles(styles)
export default class LoadingFailed extends Component {
    static propTypes = {
        classes: PropTypes.object.isRequired,
        errorText: PropTypes.any,
    };


    render() {
        const {classes, errorText} = this.props;


        return (
            <>
                <div className={classes.errorLabel}>
                    <Typography
                        color="error"
                        gutterBottom
                        variant='h5'
                        style={{'marginTop': '5rem'}}
                    >
                        Помилка при завантаженні.
                    </Typography>


                    <Typography
                        color="error"
                        variant='h6'>
                        Повідомлення: "{errorText.message || 'Сталася помилка'}" {"\n"}
                    </Typography>

                    <Typography
                        color="error"
                        variant='h6'>
                        Деталі: "{errorText.description || ''}"
                    </Typography>

                    <Typography
                        color="error"
                        variant='h5'
                        style={{'marginTop': '1rem'}}>
                        <ContactSupport upper={true}/>
                    </Typography>
                </div>
            </>
        );
    }
}