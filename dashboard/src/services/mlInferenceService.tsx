const liquidLevel = async (): Promise<any> => {
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/liquid_level`
    );
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Erro ao chamar a API:", error);
    throw error;
  }
};

const vazamento = async (): Promise<any> => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/vazamento`);
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Erro ao chamar a API:", error);
    throw error;
  }
};

const alerts = async (): Promise<any> => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/alerts`);
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Erro ao chamar a API:", error);
    throw error;
  }
};

export default { liquidLevel, vazamento, alerts };
