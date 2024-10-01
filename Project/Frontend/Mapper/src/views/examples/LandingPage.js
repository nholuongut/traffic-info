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
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardTitle,
  Container,
  Row,
  Col
} from "reactstrap";

// core components
import ExamplesNavbar from "components/Navbars/ExamplesNavbar.js";
import LandingPageHeader from "components/Headers/LandingPageHeader.js";
import DemoFooter from "components/Footers/DemoFooter.js";

function LandingPage() {
  document.documentElement.classList.remove("nav-open");
  React.useEffect(() => {
    document.body.classList.add("profile-page");
    return function cleanup() {
      document.body.classList.remove("profile-page");
    };
  });
  return (
    <>
      <ExamplesNavbar />
      <LandingPageHeader />
      <div className="main">
        <div className="section text-center">
          <Container>
            <Row>
              <Col className="ml-auto mr-auto" md="8">
                <h2 className="title">Let's talk product</h2>
                <h5 style={{fontSize:20, fontWeight:'bolder'}} className="description">
                  Traffic Jammer is a web application that allows you to control traffic close to you 
                  and manage your city through a very detailed dashboard.
                </h5>
                <br />
                <Button
                  className="btn-round"
                  color="info"
                  href="/documentation"
                >
                  See Documentation
                </Button>
              </Col>
            </Row>
            <br />
            <br />
            <Row>
              <Col md="4">
                <div className="info">
                  <div className="icon icon-info">
                    <i className="nc-icon nc-bulb-63" />
                  </div>
                  <div className="description">
                    <h4 className="info-title">Updated Traffic</h4>
                    <p style={{fontWeight:'bolder'}}>
                      Simple interface for visualizing the traffic around you, don't waste time in traffic anymore.
                    </p>
                  </div>
                </div>
              </Col>
              <Col md="4">
                <div className="info">
                  <div className="icon icon-info">
                    <i className="nc-icon nc-chart-bar-32" />
                  </div>
                  <div className="description">
                    <h4 className="info-title">Statistics</h4>
                    <p style={{fontWeight:'bolder'}}>
                      Relevant statistics concerning your city's roads including: roadbloack, traffic jams and
                      car crashes.
                    </p>
                  </div>
                </div>
              </Col>
              <Col md="4">
                <div className="info">
                  <div className="icon icon-info">
                    <i className="nc-icon nc-sun-fog-29" />
                  </div>
                  <div className="description">
                    <h4 className="info-title">Friendly design</h4>
                    <p style={{fontWeight:'bolder'}}>
                      Beautiful and easily usable interface both for clients and administration.
                    </p>
                  </div>
                </div>
              </Col>
            </Row>
          </Container>
        </div>
        <div className="section section-dark text-center">
          <Container>
            <h2 className="title">Meet the team</h2>
            <Row>
              <Col md="3">
                <Card className="card-profile card-plain">
                  <div className="card-avatar">
                    <a href="#tomas" >
                      <img
                        alt="..."
                        src={require("assets/img/tomas2.png")}
                      />
                    </a>
                  </div>
                  <CardBody>
                    <a href="#tomas" >
                      <div className="author">
                        <CardTitle tag="h4">Tomás Costa</CardTitle>
                        <h6 className="card-category">Team Manager</h6>
                      </div>
                    </a>
                    <p className="card-description text-center">
                      Teamwork is so important that it is virtually impossible
                      for you to reach the heights of your capabilities or make
                      the money that you want without becoming very good at it.
                    </p>
                  </CardBody>
                  <CardFooter className="text-center">
                    <Button
                      className="btn-just-icon btn-neutral"
                      color="link"
                      target = "_blank"
                      href="https://www.github.com/tomascostak"
                      
                    >
                      <i className="fa fa-github" />
                    </Button>
                    <Button
                      className="btn-just-icon btn-neutral ml-1"
                      color="link"
                      target = "_blank"
                      href="https://www.facebook.com/tomasoliveira.costa"
                      
                    >
                      <i className="fa fa-facebook" />
                    </Button>
                    <Button
                      className="btn-just-icon btn-neutral ml-1"
                      color="link"
                      target = "_blank"
                      href="https://www.linkedin.com/in/tomascostax"
                      
                    >
                      <i className="fa fa-linkedin" />
                    </Button>
                  </CardFooter>
                </Card>
              </Col>
              <Col md="3">
                <Card className="card-profile card-plain">
                  <div className="card-avatar">
                    <a href="#pablo" >
                      <img
                        alt="..."
                        src={require("assets/img/mota2.png")}
                      />
                    </a>
                  </div>
                  <CardBody>
                    <a href="#pablo" >
                      <div className="author">
                        <CardTitle tag="h4">Miguel Mota</CardTitle>
                        <h6 className="card-category">Product Owner</h6>
                      </div>
                    </a>
                    <p className="card-description text-center">
                      A group becomes a team when each member is sure enough of
                      himself and his contribution to praise the skill of the
                      others. No one can whistle a symphony. It takes an
                      orchestra to play it.
                    </p>
                  </CardBody>
                  <CardFooter className="text-center">
                    <Button
                      className="btn-just-icon btn-neutral"
                      color="link"
                      target = "_blank"
                      href="https://www.github.com/tomascostak"
                      
                    >
                      <i className="fa fa-github" />
                    </Button>
                    <Button
                      className="btn-just-icon btn-neutral ml-1"
                      color="link"
                      target = "_blank"
                      href="https://www.facebook.com/tomasoliveira.costa"
                      
                    >
                      <i className="fa fa-facebook" />
                    </Button>
                    <Button
                      className="btn-just-icon btn-neutral ml-1"
                      color="link"
                      target = "_blank"
                      href="https://www.linkedin.com/in/tomascostax"
                      
                    >
                      <i className="fa fa-linkedin" />
                    </Button>
                  </CardFooter>
                </Card>
              </Col>
              <Col md="3">
                <Card className="card-profile card-plain">
                  <div className="card-avatar">
                    <a href="#pedro" >
                      <img
                        alt="..."
                        src={require("assets/img/pedro.jpg")}
                      />
                    </a>
                  </div>
                  <CardBody>
                    <a href="#pedro" >
                      <div className="author">
                        <CardTitle tag="h4">Pedro Oliveira</CardTitle>
                        <h6 className="card-category">DevOps Master</h6>
                      </div>
                    </a>
                    <p className="card-description text-center">
                      A group becomes a team when each member is sure enough of
                      himself and his contribution to praise the skill of the
                      others. No one can whistle a symphony. It takes an
                      orchestra to play it.
                    </p>
                  </CardBody>
                  <CardFooter className="text-center">
                    <Button
                      className="btn-just-icon btn-neutral"
                      color="link"
                      target = "_blank"
                      href="https://www.github.com/tomascostak"
                      
                    >
                      <i className="fa fa-github" />
                    </Button>
                    <Button
                      className="btn-just-icon btn-neutral ml-1"
                      color="link"
                      target = "_blank"
                      href="https://www.facebook.com/tomasoliveira.costa"
                      
                    >
                      <i className="fa fa-facebook" />
                    </Button>
                    <Button
                      className="btn-just-icon btn-neutral ml-1"
                      color="link"
                      target = "_blank"
                      href="https://www.linkedin.com/in/tomascostax"
                      
                    >
                      <i className="fa fa-linkedin" />
                    </Button>
                  </CardFooter>
                </Card>
              </Col>
              <Col md="3">
                <Card className="card-profile card-plain">
                  <div className="card-avatar">
                    <a href="#joao" >
                      <img
                        alt="..."
                        src={require("assets/img/joao.png")}
                      />
                    </a>
                  </div>
                  <CardBody>
                    <a href="#joao" >
                      <div className="author">
                        <CardTitle tag="h4">João Silva</CardTitle>
                        <h6 className="card-category">Architecture Expert</h6>
                      </div>
                    </a>
                    <p className="card-description text-center">
                      The strength of the team is each individual member. The
                      strength of each member is the team. If you can laugh
                      together, you can work together, silence isn’t golden,
                      it’s deadly.
                    </p>
                  </CardBody>
                  <CardFooter className="text-center">
                    <Button
                      className="btn-just-icon btn-neutral"
                      color="link"
                      target = "_blank"
                      href="https://www.github.com/tomascostak"
                      
                    >
                      <i className="fa fa-github" />
                    </Button>
                    <Button
                      className="btn-just-icon btn-neutral ml-1"
                      color="link"
                      target = "_blank"
                      href="https://www.facebook.com/tomasoliveira.costa"
                      
                    >
                      <i className="fa fa-facebook" />
                    </Button>
                    <Button
                      className="btn-just-icon btn-neutral ml-1"
                      color="link"
                      target = "_blank"
                      href="https://www.linkedin.com/in/tomascostax"
                      
                    >
                      <i className="fa fa-linkedin" />
                    </Button>
                  </CardFooter>
                </Card>
              </Col>
            </Row>
          </Container>
        </div>
      </div>
      <DemoFooter />
    </>
  );
}

export default LandingPage;
