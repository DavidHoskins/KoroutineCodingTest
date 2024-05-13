import React from "react";

export class CrawlerLog extends React.Component {
    render()
    {
        return (
            <div>
            {
                this.props.data &&
                (
                    <div>
                    <h1>Explored</h1>
                    {
                        this.props.data.explored_urls.map((url, index) => (
                        <p key={index}>{url}</p>
                        ))
                    }
                    <h1>Unexplored</h1>
                    {
                        this.props.data.unexplored_urls.map((url, index) => (
                        <p key={index}>{url}</p>
                        ))
                    }
                    </div>
                )
            }
            </div>
        );
    }
}