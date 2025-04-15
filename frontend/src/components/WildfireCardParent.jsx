import React from 'react';
import WildfireCard from './WildfireCard';

const WildfireList = ({ wildfires, search_text, highlightText }) => (
  <div className="row">
    {wildfires.map(wildfire => (
      <WildfireCard
        key={wildfire.id}
        wildfire={wildfire}
        search_text={search_text}
        highlightText={highlightText}
      />
    ))}
  </div>
);

export default WildfireList;
