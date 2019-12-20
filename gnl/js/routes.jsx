import React from 'react';
// import App from './app';
import Selection from './selection';
import Label from './label';
// import Redirection from './redirection';
// import { Router, Route, browserHistory, IndexRoute } from 'react-router-3';
import { Router, Route, Switch } from 'react-router-dom';
import createHistory from 'history/createBrowserHistory';
export const history = createHistory();

const routes = () => (
  <Router history={history}>
     <Switch>
       <Route path='/selection' component = { Selection } />
       <Route path = '/label' component = { Label } />
     </Switch>
  </Router>

);
export default routes;
