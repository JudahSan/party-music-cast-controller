import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";
import CreateRoomPage from "./CreateRoomPage";
import RoomJoinPage from "./RoomJoinPage";


export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {

        }
          }
    render() {
        return (<div>
            <HomePage/>
           

        </div>);
    }
}
const appDiv = document.getElementById("app");
// Create components and pass prop(argument) modify behavior
render(<App />, appDiv);
               