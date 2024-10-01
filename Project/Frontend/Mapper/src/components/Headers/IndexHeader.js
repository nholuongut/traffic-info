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
/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container } from "reactstrap";

// core components

function IndexHeader() {
  return (
    <>
      <div
        className="page-header section-dark"
        style={{
          backgroundImage:
            "url(" + require("assets/img/grid_neon.jpg") + ")"
        }}
      >
        <div className="filter" />
        <div className="content-center" >
          <Container>
            <div className="title-brand">
              <h1 style={{fontSize: 125,
                fontWeight: 700,
                margin: 0,
                color: "#FFFFFF"}} >Traffic Jammer</h1>
            </div>
            <h2 className="presentation-subtitle text-center"
              style={{fontSize:40}}>
              Closely follow traffic for your favourite city!
            </h2>
          </Container>
        </div>
        
    </div>
  </>
  );
}

export default IndexHeader;
