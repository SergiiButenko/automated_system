import {createMuiTheme} from '@material-ui/core/styles';

export const theme = createMuiTheme({
    typography: {
        useNextVariants: true,
    },
    palette: {
        primary: {
            main: '#009688',
        }
    },
    overrides: {
        MuiCardContent: { // Name of the component ⚛️ / style sheet
            root: { // Name of the rule
                paddingLeft: 16, // Some CSS
                paddingRight: 16, // Some CSS
            },
        },
    },
});