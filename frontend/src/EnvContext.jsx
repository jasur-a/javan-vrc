import React, { createContext } from 'react';

export const Context = createContext({"form": {}});


// Create context
export const EnvContext = createContext({
  envData: {},
  setEnvData: () => {}
});

// Provider with initial State
export const EnvProvider = ({ envData, children }) => {
    return (
      <EnvContext.Provider value={{ envData }}>{children}</EnvContext.Provider>
    );
  };
  
  export default EnvProvider;