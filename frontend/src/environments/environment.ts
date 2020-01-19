
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'rhytah.auth0.com', // the auth0 domain prefix
    audience: 'capstone', // the api audience set for the auth0 app
    clientId: '6zpukCge2vIX2RZpwTlBpBqL00Fg2pHA', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running angular application. 
  }
};
