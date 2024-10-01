/*!

=========================================================
* Paper Kit React - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/paper-kit-react

* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/paper-kit-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React, { Component } from "react";
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
// reactstrap components
import { Button, Form, Input, Container, Row, Col } from "reactstrap";
import { Text } from 'react-konva';
import "../../../node_modules/react-datepicker/dist/react-datepicker.css"
// core components
import BlackNavbar from "components/Navbars/BlackNavbar.js";
import { FormErrors } from './MapFormError.js';

const API = 'http://192.168.160.237:8000/';
const DEFAULT_QUERY = 'all_streets/';
const ALL_CITIES = 'available_cities/';
const POST_STREET = 'street/';

//Fazer as stats como class independende


class Admin extends Component {

  constructor(props) {
    super(props);
    this.state = {
      streetname: '',
      beginX: 0,
      beginY: 0,
      endX: 0,
      endY: 0,
      city: '',
      error_log: {streetname: '', beginX: '', endX: '', beginY: '', endY: '', city: '', coords: ''},
      name_valid: false,
      beginX_valid: false,
      beginY_valid: false,
      endX_valid: false,
      endY_valid: false,
      coord_valid: false,
      city_valid: false,
      valid: false,
      all_cities: []
    }
  }

  fetchAllCities(){
    fetch(API+ALL_CITIES, { headers: {'Content-Type': 'application/json'}}).
      then(resp => resp.json()).
      then(responseData => {
        return responseData;
      })
      .then(data => {this.setState({
        all_cities : data
      })
    });
  }

  //date-format: AAAA-MM-DD

  componentDidMount() {
    //somting in here
  }

  componentWillUnmount() {
    //sumting heya
  }

  postStreet = () =>{
    console.log("posting to ", + API + POST_STREET)
    let fetchBody = JSON.stringify({
      "name": this.state.streetname,
      "beginning_coords": [
        parseInt(this.state.beginX),
        parseInt(this.state.beginY)
      ],
      "ending_coords": [
        parseInt(this.state.endX),
        parseInt(this.state.endY)
      ],
      "city": this.state.city
    })

    fetch( API + POST_STREET, {  
      method: 'POST',
      headers: {'Content-Type': 'text/plain'} ,
      body: fetchBody
    })
    .then( (response) => response.json())
    .then( responseJson => {
      if(responseJson.success != 0){
        alert("Street successfully created!")
      }
      else{
        alert("Street creation failed! Try again.")
      }
    })
    .catch((error) => {
      console.log(error);
    });

  }

  handleUserInput = async (e) => {
    const name = e.target.name;
    const value = e.target.value;
    console.log("Setting " + name)
    console.log("as " + value)
    await this.setState({[name]: value}, () => {this.validateData(); });
  }


  validateData = () => {
    this.fetchAllCities();
    
    this.state.name_valid = this.state.streetname.match(/^[a-zA-Z ]{2,80}$/);
    this.state.error_log.streetname = (!this.state.name_valid)? "You inserted an invalid name\n":"" ;
    
    this.state.beginX_valid = !Number.isNaN(this.state.beginX);
    this.state.error_log.beginX = (!this.state.beginX_valid)? "Begining Coordinate of X is not a number\n":"";
    
    this.state.beginY_valid = !Number.isNaN(this.state.beginY);
    this.state.error_log.beginY = (!this.state.beginY_valid)? "Begining Coordinate of Y is not a number\n":"";
    
    this.state.endX_valid = !Number.isNaN(this.state.endX);
    this.state.error_log.endX = (!this.state.endX_valid)? "Ending Coordinate of X is not a number\n":"";
    
    this.state.endY_valid = !Number.isNaN(this.state.endY);
    this.state.error_log.endY = (!this.state.endY_valid)? "Ending Coordinate of Y is not a number\n":"";
    
    this.state.coord_valid = this.state.beginX != this.state.endX || this.state.beginY != this.state.endY;
    this.state.error_log.coords = (!this.state.coord_valid)? "Both begining and ending coordinates are the same\n":"";
    
    this.state.city_valid = this.state.all_cities.includes(this.state.city);
    this.state.error_log.city = (!this.state.city_valid)? "The cities you entered are invalid, you can only pick between " + this.state.all_cities + "\n":"";
    
    this.state.valid = this.state.name_valid && this.state.beginX_valid && this.state.beginY_valid && this.state.endX_valid && this.state.endY_valid && this.state.coord_valid && this.state.city_valid;
        
  }

  getDataStats = () => {
    console.log("Making request to statistics")
    var final_url = '';
    fetch( API + final_url, {  
      method: 'POST',
      headers: {'Content-Type': 'application/json'} 
    }).
      then(resp => {
        console.log(JSON.stringify(resp.body))
        return resp;
      })
      .then(data => {this.setState({
        //dataSourceStats : [data]
      })
    });
  }

  render() {
    return (
      <>
        <BlackNavbar />
        <div
          className="page-header"
          data-parallax={true}
          style={{
            backgroundColor:'rgba(255,255,255,1)',
          }}
        >
            <Container style={{display:'flex',flex:1,flexDirection:'column'}}>
              <React.Fragment>
                <Typography variant="h6" gutterBottom>
                  Map Address
                </Typography>
                <Grid container spacing={3}>
                  <Grid item xs={12}>
                    <TextField
                      required
                      id="streetname"
                      name="streetname"
                      label="Street name"
                      fullWidth
                      onChange={(event) => this.handleUserInput(event)}
                      value={this.state.name}
                      
                      autoComplete="Rua"
                    />
                  </Grid>
                  <Grid item xs={6} sm={3}>
                      <TextField
                      required
                      id="beginX"
                      name="beginX"
                      label="X coord to start"
                      type="number"
                      fullWidth
                      onChange={(event) => this.handleUserInput(event)}
                      value={this.state.beginX}
                      autoComplete="0"
                      />
                  </Grid>
                  <Grid item xs={6} sm={3}>
                      <TextField
                      required
                      id="beginY"
                      name="beginY"
                      label="Y coord to start"
                      type="number"
                      fullWidth
                      onChange={(event) => this.handleUserInput(event)}
                      value={this.state.beginY}
                      autoComplete="0"
                      />
                  </Grid>
                  <Grid item xs={6} sm={3}>
                      <TextField
                      required
                      id="endX"
                      name="endX"
                      label="X coord to end"
                      type="number"
                      fullWidth
                      onChange={(event) => this.handleUserInput(event)}
                      value={this.state.endX}
                      autoComplete="1000"
                      />
                  </Grid>
                  <Grid item xs={6} sm={3}>
                      <TextField
                      required
                      id="endY"
                      name="endY"
                      label="Y coord to end"
                      fullWidth
                      type="number"
                      onChange={(event) => this.handleUserInput(event)}
                      value={this.state.endY}
                      autoComplete="100"
                      />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      required
                      id="city"
                      name="city"
                      label="City"
                      fullWidth
                      onChange={(event) => this.handleUserInput(event)}
                      value={this.state.city}
                      autoComplete="Cidade "
                    />
                  </Grid>
                </Grid>
                <Button
                    variant="contained"
                    color="primary"
                    disabled={!this.state.valid}
                    onClick={() => this.postStreet()}
                  >Submit</Button>  
                <Grid xs={6} sm={3}>
                    <TextField
                      required
                      id="city"
                      name="city"
                      label="City"
                      fullWidth
                      onChange={(event) => this.handleUserInput(event)}
                      value={this.state.city}
                      autoComplete="Cidade "
                    />
                  </Grid>
              </React.Fragment>
            </Container>
            
        </div>
        <div className="panel panel-default">
          <FormErrors formErrors={this.state.error_log} />
        </div>
    </>
    )
  }
}

export default Admin;
