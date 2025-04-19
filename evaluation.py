# evaluation.py
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score

class CVEvaluator:
    def __init__(self, ground_truth_path, results_dir):
        """
        Initialize evaluator with ground truth data and results directory
        
        Args:
            ground_truth_path: Path to JSON file with labeled CV data
            results_dir: Directory containing model results
        """
        self.ground_truth = self._load_ground_truth(ground_truth_path)
        self.results_dir = results_dir
        self.models = ['llama3', 'mistral', 'phi']
        self.fields = ['name', 'email', 'phone', 'education', 'experience', 'skills']
        
    def _load_ground_truth(self, path):
        """Load ground truth data from JSON file"""
        with open(path, 'r') as f:
            return json.load(f)
    
    def _string_match_score(self, pred, truth):
        """Basic string matching score with normalization"""
        if not pred or not truth:
            return 0
        
        # Normalize strings
        pred = pred.lower().strip()
        truth = truth.lower().strip()
        
        # Exact match
        if pred == truth:
            return 1
        
        # Partial match
        if pred in truth or truth in pred:
            return 0.5
            
        return 0
    
    def _list_match_score(self, pred_list, truth_list):
        """Compute matching score for lists (skills, education, experience)"""
        if not pred_list or not truth_list:
            return 0
            
        if not isinstance(pred_list, list) or not isinstance(truth_list, list):
            return 0
            
        # For simple lists like skills
        if isinstance(pred_list[0], str) and isinstance(truth_list[0], str):
            # Count matches
            matches = sum(1 for item in pred_list if any(self._string_match_score(item, truth_item) > 0.5 for truth_item in truth_list))
            return matches / max(len(truth_list), 1)
        
        # For complex lists (education, experience)
        # This is simplified - you would ideally need a more sophisticated matching
        return 0.5  # Placeholder
    
    def evaluate_cv(self, cv_id, model_results):
        """
        Evaluate a single CV's extraction results against ground truth
        
        Args:
            cv_id: ID of the CV to evaluate
            model_results: Dictionary of model results for this CV
            
        Returns:
            Dictionary with scores for each field and model
        """
        ground_truth = self.ground_truth.get(cv_id, {})
        if not ground_truth:
            return None
            
        scores = {}
        for model, result in model_results.items():
            scores[model] = {}
            
            # Evaluate simple string fields
            for field in ['name', 'email', 'phone']:
                pred = result.get(field, '')
                truth = ground_truth.get(field, '')
                scores[model][field] = self._string_match_score(pred, truth)
            
            # Evaluate list fields
            for field in ['skills']:
                pred_list = result.get(field, [])
                truth_list = ground_truth.get(field, [])
                scores[model][field] = self._list_match_score(pred_list, truth_list)
                
            # Complex fields would need more sophisticated evaluation
            for field in ['education', 'experience']:
                scores[model][field] = 0.5  # Placeholder
                
            # Overall score (average)
            scores[model]['overall'] = sum(scores[model].values()) / len(scores[model])
            
        return scores
    
    def generate_report(self, evaluation_results):
        """
        Generate metrics and charts from evaluation results
        
        Args:
            evaluation_results: Dictionary of scores by CV and model
            
        Returns:
            Pandas DataFrame with results and saves charts
        """
        # Aggregate scores across all CVs
        agg_scores = {model: {field: 0 for field in self.fields + ['overall']} for model in self.models}
        cv_count = len(evaluation_results)
        
        for cv_result in evaluation_results.values():
            for model in self.models:
                for field in self.fields + ['overall']:
                    agg_scores[model][field] += cv_result[model][field] / cv_count
        
        # Create DataFrame
        df = pd.DataFrame({
            model: {field: agg_scores[model][field] for field in self.fields + ['overall']}
            for model in self.models
        })
        
        # Generate charts
        self._generate_charts(df)
        
        return df
    
    def _generate_charts(self, df):
        """Generate comparison charts"""
        # Bar chart
        ax = df.plot(kind='bar', figsize=(12, 6))
        ax.set_xlabel('Fields')
        ax.set_ylabel('Score')
        ax.set_title('LLM Model Performance Comparison by Field')
        ax.legend(title='Models')
        plt.tight_layout()
        plt.savefig('model_comparison_by_field.png')
        
        # Radar chart for overall performance
        overall_df = df.loc['overall'].to_frame().T
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Number of variables
        categories = list(overall_df.columns)
        N = len(categories)
        
        # Create angles for each variable
        angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Plot each model
        for model in overall_df.index:
            values = overall_df.loc[model].values.flatten().tolist()
            values += values[:1]  # Close the loop
            
            ax.plot(angles, values, linewidth=2, linestyle='solid', label=model)
            ax.fill(angles, values, alpha=0.1)
        
        # Set labels and title
        plt.xticks(angles[:-1], categories)
        ax.set_title('Overall Model Performance')
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        plt.savefig('model_overall_performance.png')