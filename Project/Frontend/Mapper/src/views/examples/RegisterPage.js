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
import React from "react";

// reactstrap components
import { Button, Form, Input, Container, Row, Col } from "reactstrap";

// core components
import ExamplesNavbar from "components/Navbars/ExamplesNavbar.js";

function submitForm(formValue) {
  alert("Login Success")
  if (true){
    window.location.replace('/index');
  }
}

function RegisterPage() {
  document.documentElement.classList.remove("nav-open");
  React.useEffect(() => {
    document.body.classList.add("register-page");
    return function cleanup() {
      document.body.classList.remove("register-page");
    };
  });
  return (
    <>
      <ExamplesNavbar />
      <div
        className="page-header"
        data-parallax={true}
y        style={{
          backgroundImage: "url(" + require("assets/img/grid_neon2.png") + ")",
          
        }}
      >
        
        <div style={{background: "black"}} />
        <Container>
          <Row>
            <Col className="ml-auto mr-auto" lg="4" >
                <h3 style={{textAlign:'center', fontWeight:'bold', fontSize:30}} className="title mx-auto">Sign In</h3>
                <Form className="register-form" color="primary">
                  <label color="neutral">Email</label>
                  <Input placeholder="Email" type="email" />
                  <label color="neutral">Password</label>
                  <Input placeholder="Password" type="password" value=""/>
                  <Button style={{marginTop:10}} block className="btn-round" onClick={e => submitForm()} color="primary">
                    Login
                  </Button>
                </Form>
                <div className="forgot">
                  <Button
                    className="btn-link"
                    color="neutral"
                    href="/index"
                  >
                    Forgot password?
                  </Button>
                </div>
            </Col>
          </Row>
        </Container>

      </div>
    </>
  );
}

export default RegisterPage;
