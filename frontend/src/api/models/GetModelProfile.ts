import { useQuery, UseQueryResult } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import axios from '../../utils/axios';
import { GET_MODEL_PROFILE_API } from '../apis';
import {
  ModelProfile,
  ModelProfileCategoricalFeature,
  ModelProfileNumericalFeature,
  ModelProfileTextFeature
} from '../../@types/model';

interface GetModelProfileParams {
  id: string;
}

interface GetModelProfileResponse {
  total_features: number;
  total_data_rows: number;
  total_duplicates: number;
  total_missing_values: number;
  percentage_duplicates: number;
  percentage_missing_values: number;
  features: {
    text: {
      total: number;
      data: {
        name: string;
        distinct_count: number;
        distinct_percentage: number;
        missing_count: number;
        missing_percentage: number;
        word_counts: Record<string, number>;
        mean_length: number;
        min_length: number;
        max_length: number;
        histogram: Record<string, number>;
      }[];
    };
    numerical: {
      total: number;
      data: {
        name: string;
        distinct_count: number;
        distinct_percentage: number;
        missing_count: number;
        missing_percentage: number;
        zeroes_count: number;
        zeros_percentage: number;
        minimum: number;
        maximum: number;
        mean: number;
        std: number;
        variance: number;
        '5%': number;
        '25%': number;
        '50%': number;
        '75%': number;
        '95%': number;
        kurtosis: number;
        skewness: number;
        histogram: {
          counts: number[];
          bin_edges: number[];
        };
      }[];
    };
    categorical: {
      total: number;
      data: {
        name: string;
        distinct_count: number;
        distinct_percentage: number;
        missing_count: number;
        missing_percentage: number;
        histogram: Record<string, number>;
        histogram_value_type: string;
      }[];
    };
  };
}

interface ResultData extends ModelProfile {
  data: GetModelProfileResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

type ModelProfileQuery = UseQueryResult<ResultData, unknown>;

interface UseModelInfo {
  (params: GetModelProfileParams): ModelProfileQuery;
}

export const useModelProfile: UseModelInfo = (params) => {
  return useQuery(['model.profile', params], queryModels, {
    refetchOnWindowFocus: false
  });

  async function queryModels() {
    const apiParams = {
      model_id: params.id
    };
    const response = await axios.get<GetModelProfileResponse>(GET_MODEL_PROFILE_API, {
      params: apiParams
    });
    const {
      total_features,
      total_data_rows,
      total_duplicates,
      total_missing_values,
      percentage_duplicates,
      percentage_missing_values,
      features: { text, categorical, numerical }
    } = response.data;

    const textData = text?.data?.map(
      (tf: GetModelProfileResponse['features']['text']['data'][0]): ModelProfileTextFeature => ({
        name: tf?.name || '',
        distinctCount: tf?.distinct_count || 0,
        distinctPercentage: tf?.distinct_percentage || 0,
        missingCount: tf?.missing_count || 0,
        missingPercentage: tf?.missing_percentage || 0,
        wordCounts: tf?.word_counts || 0,
        meanLength: tf?.mean_length || 0,
        minLength: tf?.min_length || 0,
        maxLength: tf?.max_length || 0,
        histogram: tf?.histogram || {}
      })
    );

    const categoricalData = categorical?.data?.map(
      (
        cf: GetModelProfileResponse['features']['categorical']['data'][0]
      ): ModelProfileCategoricalFeature => ({
        name: cf?.name || '',
        distinctCount: cf?.distinct_count || 0,
        distinctPercentage: cf?.distinct_percentage || 0,
        missingCount: cf?.missing_count || 0,
        missingPercentage: cf?.missing_percentage || 0,
        histogram: cf?.histogram || {},
        histogramValueType: cf?.histogram_value_type || ''
      })
    );

    const numericalData = numerical?.data?.map(
      (
        nf: GetModelProfileResponse['features']['numerical']['data'][0]
      ): ModelProfileNumericalFeature => ({
        name: nf?.name || '',
        distinctCount: nf?.distinct_count || 0,
        distinctPercentage: nf?.distinct_percentage || 0,
        missingCount: nf?.missing_count || 0,
        missingPercentage: nf?.missing_percentage || 0,
        zeroesCount: nf?.zeroes_count || 0,
        zeroesPercentage: nf?.zeros_percentage || 0,
        minimum: nf?.minimum || 0,
        maximum: nf?.maximum || 0,
        mean: nf?.mean || 0,
        std: nf?.std || 0,
        variance: nf?.variance || 0,
        '5%': nf?.['5%'] || 0,
        '25%': nf?.['25%'] || 0,
        '50%': nf?.['50%'] || 0,
        '75%': nf?.['75%'] || 0,
        '95%': nf?.['95%'] || 0,
        kurtosis: nf?.kurtosis || 0,
        skewness: nf?.skewness || 0,
        histogram: {
          counts: nf?.histogram?.counts || [],
          binEdges: nf?.histogram?.bin_edges || []
        }
      })
    );

    return {
      ...response,
      totalFeatures: total_features || 0,
      totalDataRows: total_data_rows || 0,
      totalDuplicates: total_duplicates || 0,
      totalMissingValues: total_missing_values || 0,
      percentageDuplicates: percentage_duplicates || 0,
      percentageMissingValues: percentage_missing_values || 0,
      text: {
        total: text?.total || 0,
        data: textData
      },
      categorical: {
        total: text?.total || 0,
        data: categoricalData
      },
      numerical: {
        total: text?.total || 0,
        data: numericalData
      }
    };
  }
};
