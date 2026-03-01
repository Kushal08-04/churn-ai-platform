import shap

def explain(model, features):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(features)
    return shap_values.tolist()