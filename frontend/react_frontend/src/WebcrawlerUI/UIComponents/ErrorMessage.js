import React from "react";

export class ErrorMessage extends React.Component {
    render()
    {
        return <p style={{color:"red"}}>{this.props.error_message}</p>
    }
}