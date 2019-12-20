// import React from "react";
import ReactDOM from "react-dom";
import routes from './routes';
const renderApp = (appRoutes) => {
    ReactDOM.render(appRoutes, document.getElementById('reactEntry'));
};
renderApp(routes());
