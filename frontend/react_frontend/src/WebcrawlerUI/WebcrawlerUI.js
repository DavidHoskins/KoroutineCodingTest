import React from 'react';
import {ErrorMessage} from './UIComponents/ErrorMessage.js';
import { WebsiteForm } from './UIComponents/WebsiteForm.js';
import { CrawlerLog } from './UIComponents/CrawlerLog.js';

// Regex for confirming website matches required format before submitting to server.
const regex = /^(https?:\/\/)(www\.)?[\w-]+\.(?:com|co\.uk|org|net)$/;

const websocket_url = "ws://0.0.0.0:";
const websocket_port = "8000";

export class WebcrawlerUI extends React.Component {
    constructor(props){
        super(props);
        this.state = {website: "", data: "", error_message: null};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.socket = null
    }

    handleChange(event) 
    {    
        this.setState(prevState => ({
        website: event.target.value
        }));
    }

    handleSubmit(event)
    {
        event.preventDefault();
        if(!regex.test(this.state.website))
        {
            this.setState(
                {
                    error_message: "Error with URL please reformat, we require https:// or http:// at the front a full www. and ending in .com, .co.uk, .org or .net"
                }
            );
            return;
        }
        if(this.state.error_message != null)
            this.setState({error_message: null});

        // Check connection closed before opening new connection
        try
        {
            if (this.socket != null)
                this.socket.close();

            this.socket = new WebSocket(websocket_url + websocket_port);
        }
        catch(error)
        {
            console.log(error);
        }

        // Connection opened
        this.socket.addEventListener("open", (event) => {
        try
        {
            this.socket.send(this.state.website);
        }
        catch(error)
        {
            console.log(error);
        }
        })

        // Listen for messages
        this.socket.addEventListener("message", (event) => {
        try
        {
            let jsonData = JSON.parse(event.data);
            this.setState({data: jsonData});
        }
        catch(error)
        {
            console.log(error);
        }
        })
    }

    render() {
        return (
        <div>
            <WebsiteForm handleSubmit={this.handleSubmit} website={this.state.website} handleChange={this.handleChange}/>
            <ErrorMessage error_message={this.state.error_message}/>
            <CrawlerLog data={this.state.data}/>
        </div>
        )
    }
}