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
import { Link } from "react-router-dom";
// nodejs library that concatenates strings
import classnames from "classnames";

// reactstrap components
import {
  Collapse,
  NavbarBrand,
  Navbar,
  NavItem,
  NavLink,
  Nav,
  Button,
  Container
} from "reactstrap";

function BlackNavbar() {
  const [navbarColor, setNavbarColor] = React.useState("");
  const [navbarCollapse, setNavbarCollapse] = React.useState(false);

  const toggleNavbarCollapse = () => {
    setNavbarCollapse(!navbarCollapse);
    document.documentElement.classList.toggle("nav-open");
  };

  React.useEffect(() => {
    const updateNavbarColor = () => {
      if (
        document.documentElement.scrollTop > 299 ||
        document.body.scrollTop > 299
      ) {
        setNavbarColor("navbar-transparent");
      } else if (
        document.documentElement.scrollTop < 300 ||
        document.body.scrollTop < 300
      ) {
        setNavbarColor("");
      }
    };

    window.addEventListener("scroll", updateNavbarColor);

    return function cleanup() {
      window.removeEventListener("scroll", updateNavbarColor);
    };
  });
  return (
    <Navbar
      className={classnames("fixed-top", navbarColor)}
      color-on-scroll="300"
      expand="lg"
    >
      <Container>
        <div className="navbar-translate">
          <NavbarBrand
            data-placement="bottom"
            to="/index"
            title="Traffic Jammer"
            tag={Link}
          >
            Traffic Jammer
          </NavbarBrand>
          <button
            aria-expanded={navbarCollapse}
            className={classnames("navbar-toggler navbar-toggler", {
              toggled: navbarCollapse
            })}
            onClick={toggleNavbarCollapse}
          >
            <span className="navbar-toggler-bar bar1" />
            <span className="navbar-toggler-bar bar2" />
            <span className="navbar-toggler-bar bar3" />
          </button>
        </div>
        <Collapse
          className="justify-content-end"
          navbar
          isOpen={navbarCollapse}
        >
          <Nav navbar>
            <NavItem>
              <NavLink
                data-placement="bottom"
                href="https://gitlab.com/myiesgroup/iesproject_trafficjammer"
                target="_blank"
                title="Follow on Gitlab"
              >
                <i className="fa fa-gitlab" />
                <p className="d-lg-none">Gitlab</p>
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink to="/dashboard" tag={Link}>
                <i className="nc-icon nc-chart-bar-32" /> Dashboard
              </NavLink>
            </NavItem>  
            <NavItem>
              <NavLink to="/admin" tag={Link}>
                <i className="nc-icon nc-chart-bar-32" /> Administration
              </NavLink>
            </NavItem>  
            <NavItem> 
              <NavLink
                href="https://gitlab.com/myiesgroup/iesproject_trafficjammer/blob/master/README.md"
                target="_blank"
              >
                <i className="nc-icon nc-book-bookmark" /> Documentation
              </NavLink>
            </NavItem>
            <NavItem>
              <Button
                className="btn-round"
                size = "md"
                color="primary"
                href="/app"
                target="_blank"
              >
                Traffic WEB
              </Button>
            </NavItem>

          </Nav>
        </Collapse>
      </Container>
    </Navbar>
  );
}

export default BlackNavbar;
