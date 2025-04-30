import streamlit as st
from core.config import Config
from core.src.agent import Agent
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import base64
import io

agent = Agent()

class Helper:
    def __init__(self, data: pd.DataFrame):
        self.df = data

    def run(self, user_reuqest):
        success_function_info, function_name, function_parameters = agent.process_user_request(user_request=user_reuqest)
        if success_function_info:
            success_request, message, data, graph = self.map_json_to_function(function_name, function_parameters)
            return message

    def check_cols_in_dataframe(self, cols):
        df = self.df
        # Edge Cases
        if cols is None or cols == []:
            return True
        df_columns = df.columns
        
        for col in cols:
            if col not in df_columns:
                return False
        return True

    def convert_subset_to_message(self, subset):
        return subset if subset not in [None, []] else 'all'

    '''
    The funcitons below return success (bool), message (str), processed_data (pandas.DataFrame), image
    '''
    def remove_duplicate_values(self, subset, keep):
        df = self.df
        if keep not in ['first', 'last', False]:
            return False, f'Keep is not recognized: {keep}', None, None
        
        if self.check_cols_in_dataframe(subset):
            try:
                return_message = f'Here is your data with duplicate values remove in subset: {self.convert_subset_to_message(subset)}, keep: {keep}'
                return True, return_message, df.drop_duplicates(subset=subset, keep=keep), None
            except Exception as e:
                return False, e, None, None
        else:
            return False, f'Columns not in the DataFrame: {subset}', None, None
        
    def fill_missing_values(self, subset, metric):
        df = self.df
        if metric not in ['mean', 'median', 'mode']:
            return False, f'Metric is not recognized: {metric}', None, None
        
        if self.check_cols_in_dataframe(subset):
            try:
                return_message = f'Here is your data with missing values remove in subset: {self.convert_subset_to_message(subset)}, metric: {metric}'
                df_result = df.copy()
                
                for col in subset:
                    if metric == 'mean':
                        fill_value = round(df_result[col].mean(), 3)
                    elif metric == 'median':
                        fill_value = round(df_result[col].median(), 3)
                    elif metric == 'mode':
                        fill_value = df_result[col].mode()
                    df_result[col].fillna(fill_value, inplace=True)
                return True, return_message, df_result, None
            except Exception as e:
                return False, e, None, None
        else:
            return False, f'Columns not in the DataFrame: {subset}', None, None
        
        
    def perform_correlation_analysis(self, subset):
        df = self.df
        if self.check_cols_in_dataframe(subset):
            try:
                corr = df[subset].corr()
                # plt.figure()
                # sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
                # plt.title('Correlation Heatmap')
                # buf = io.BytesIO()
                # plt.savefig(buf, format='png')
                # plt.close()
                # buf.seek(0)
                # img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                fig, ax = plt.subplots()
                sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
                ax.set_title('Correlation Heatmap')
                st.pyplot(fig)
                return True, f'Here is the correlation analysis in subset: {self.convert_subset_to_message(subset)}', corr, None
                # return True, f'Here is the correlation analysis in subset: {self.convert_subset_to_message(subset)}', corr, img_base64
            except Exception as e:
                return False, e, None, None
        else:
            return False, f'Columns not in the DataFrame: {subset}', None, None
        
    def perform_dimensionality_reduction(self, features, target):
        df = self.df
        subset = features.append(target)
        
        if self.check_cols_in_dataframe(subset):
            try:
                return_message = f'Here is the pca result of features: {features}, target: {target}'
                # PCA
                X = df[features]
                pca = PCA(n_components=2)
                X_pca = pca.fit_transform(X)
                pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'], index=df.index)
                y = df[target]
                
                # Plot
                # plt.figure(figsize=(8,6))
                # sns.scatterplot(x='PC1', y='PC2', hue=y, palette='viridis', data=pca_df.join(y))
                # plt.title('PCA Scatter Plot (PC1 vs PC2)')
                # plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.2f}% variance)')
                # plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.2f}% variance)')
                # plt.legend(title=target)

                with st.chat_message("assistant"):
                    st.write("Here is your PCA scatter plot:")

                    fig = plt.figure(figsize=(8, 6))
                    sns.scatterplot(
                        x='PC1', 
                        y='PC2', 
                        hue=y, 
                        palette='viridis', 
                        data=pca_df.join(y)
                    )
                    plt.title('PCA Scatter Plot (PC1 vs PC2)')
                    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.2f}% variance)')
                    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.2f}% variance)')
                    plt.legend(title=target)

                    st.pyplot(fig)

                
                # buf = io.BytesIO()
                # plt.savefig(buf, format='png')
                # plt.close()
                # buf.seek(0)
                # img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                
                pca_params = {
                    'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
                    'components': pca.components_.tolist()
                }
                return True, return_message, [pca_df, y, pca_params], None
                # return True, return_message, [pca_df, y, pca_params], img_base64 
            except Exception as e:
                return False, e, None, None
        else:
            return False, f'Columns not in the DataFrame: {subset}', None, None
            
    def map_json_to_function(self, function_name, function_parameters):
        df = self.df
        if function_name == 'remove_duplicate_values':
            return self.remove_duplicate_values(subset=function_parameters['subset'], keep=function_parameters['keep'])
        elif function_name == 'fill_missing_values':
            return self.fill_missing_values(subset=function_parameters['subset'], metric=function_parameters['metric'])
        elif function_name == 'perform_correlation_analysis':
            return self.perform_correlation_analysis(subset=function_parameters['subset'])
        elif function_name == 'perform_dimensionality_reduction':
            return self.perform_dimensionality_reduction(features=function_parameters['features'], target=function_parameters['target'])
        else:
            return False, f'No function recognized.', None, None
        
        