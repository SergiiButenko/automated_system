import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import * as actionCreators from '../../actions/device';
import Slider from '@material-ui/lab/Slider';
import Collapse from '@material-ui/core/Collapse';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import AccessTime from '@material-ui/icons/AccessTime';
import Iso from '@material-ui/icons/Iso';
import deepPurple from '@material-ui/core/colors/deepPurple';
import classNames from 'classnames';


const styles = theme => ({
    card: {
        minWidth: 275,
        marginBottom: theme.spacing.unit,
    },
    cardSelected: {
        boxShadow: '0 0 0 3px #8dbdf7',
        background: '#dae7f7',
    },
    content: {
        minWidth: 275,
        marginBottom: 0,
        paddingBottom: theme.spacing.unit - 8,
    },
    title: {
        marginBottom: 5,
        flex: 1,
        display: 'inline',
    },
    pos: {
        marginBottom: 12,
    },
    button: {
        margin: 0,
        flex: 1,
    },
    slider_root: {
        width: '10%',
    },
    slider: {
        padding: '16px 0px',
        marginRight: theme.spacing.unit * 2,
    },
    minutes: {
        marginBottom: 5,
        marginLeft: '3rem',
        flex: 1,
        display: 'inline',
    },
    expandMore: {
        transform: 'rotate(360deg)',
        transition: '300ms transform',
    },
    expandMore_selected: {
        transform: 'rotate(180deg)',
        transition: '300ms transform',
    },
    avatar: {
        margin: 10,
    },
    purpleAvatar: {
        margin: 10,
        color: '#fff',
        backgroundColor: deepPurple[500],
    },
    row: {
        display: 'flex',
        justifyContent: 'center',
    },
});

class ControlCard extends React.Component {

    state = {
        selected: 0,
        value_minutes: 15,
        value_qnt: 2,
        collapsed: false,
    };

    toggleSelected = () => {
        let {dispatch} = this.props;
        // let action = actionCreators.set_state(this.id, !this.state.selected);
        // dispatch(action);

        this.setState({
            selected: !this.state.selected,
        });

        this.setState({
            collapsed: false,
        });
    };

    setSelected = () => {
        let {dispatch} = this.props;
        let action = actionCreators.set_state(this.id, 1);
        dispatch(action);

        this.setState({
            selected: 1,
        });
    };

    handleCollapse = () => {
        this.setState(state => ({collapsed: !state.collapsed}));
    };

    handleChangeMinutes = (event, value_minutes) => {
        this.setState({value_minutes});
    };

    handleChangeQnt = (event, value_qnt) => {
        this.setState({value_qnt});
    };

    constructor(props) {
        super(props);
    }


    render() {
        const {classes} = this.props;
        const {value_minutes, value_qnt, selected, collapsed} = this.state;

        return (
            <>
                <Card className={classNames(classes.card, this.state.selected && classes.cardSelected)}>
                    <CardContent className={classes.content}>
                        <Grid item
                            container
                            direction="row"
                            spacing={16}
                            className={classes.header_grid}
                            onClick={this.toggleSelected}>
                            <Grid item>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Томати
                                </Typography>
                            </Grid>
                        </Grid>
                        <Grid item container direction="row" spacing={16} onClick={this.handleCollapse}>
                            <Grid item>
                                <Typography component="p">Полити {value_qnt} {value_qnt === 1 ? 'раз, ' : 'раза по'} {value_minutes} хв</Typography>
                            </Grid>
                            <Grid item xs>
                                <ExpandMoreIcon
                                    className={collapsed === 1 ? classes.expandMore_selected : classes.expandMore}/>
                            </Grid>
                        </Grid>
                        <Collapse in={collapsed}>
                            <Grid item container direction="row" spacing={16} justify="center"
                                alignItems="center">
                                <Grid item xs>
                                    <AccessTime/>
                                </Grid>
                                <Grid item xs={10}>
                                    <Slider
                                        classes={{container: classes.slider}}
                                        value={value_minutes}
                                        min={10}
                                        max={20}
                                        step={5}
                                        onChange={this.handleChangeMinutes}
                                        onDragStart={this.setSelected}
                                    />
                                </Grid>
                            </Grid>
                            <Grid item container direction="row" spacing={16} justify="center"
                                alignItems="center">
                                <Grid item xs>
                                    <Iso/>
                                </Grid>
                                <Grid item xs={10}>
                                    <Slider
                                        classes={{container: classes.slider}}
                                        value={value_qnt}
                                        min={1}
                                        max={3}
                                        step={1}
                                        onChange={this.handleChangeQnt}
                                        onDragStart={this.setSelected}
                                    />
                                </Grid>
                            </Grid>
                        </Collapse>
                    </CardContent>

                    <CardActions>
                        <Button
                            color="primary"
                            className={classes.button}
                            onClick={this.toggleSelected}
                        >
                            {selected === 1 ? 'Не поливати' : 'Обрати'}
                        </Button>
                    </CardActions>
                </Card>
            </>
        );
    }
}

ControlCard.propTypes = {
    classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(ControlCard);
