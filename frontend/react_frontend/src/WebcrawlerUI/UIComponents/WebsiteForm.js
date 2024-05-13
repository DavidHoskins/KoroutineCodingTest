import React from "react";

export class WebsiteForm extends React.Component {
    render()
    {
        return (
            <form onSubmit={this.props.handleSubmit}>        
                <label>
                Website:
                <input type="text" value={this.props.website} onChange={this.props.handleChange} />        
                </label>
                <input type="submit" value="Submit" />
            </form>
        );
    }
}