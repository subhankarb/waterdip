export const loadState = () => {
  try {
    const data = localStorage.getItem('state');
    if (data === null) return {};
    return JSON.parse(data);
  } catch (error) {
    return undefined;
  }
};

export const saveState = (state: any): any => {
  try {
    const data = JSON.stringify(state);
    localStorage.setItem('state', data);
  } catch (error) {
    return undefined;
  }
  return true;
};
