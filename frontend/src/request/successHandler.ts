import { notification } from 'antd';
import { AxiosResponse } from 'axios';
import codeMessage from './codeMessage';
import { RequestHandlerOptions } from './types';

/**
 * Handle successful API responses
 * @param response - Axios response object
 * @param options - Options for notification behavior
 */
const successHandler = (
  response: AxiosResponse, 
  options: RequestHandlerOptions = { notifyOnSuccess: false, notifyOnFailed: true }
): void => {
  const { data } = response;
  if (data && data.success === true) {
    const message = response.data && data.message;
    const successText = message || codeMessage[response.status];

    if (options.notifyOnSuccess) {
      notification.config({
        duration: 2,
        maxCount: 2,
      });
      notification.success({
        message: `Request success`,
        description: successText,
      });
    }
  } else {
    const message = response.data && data.message;
    const errorText = message || codeMessage[response.status];
    const { status } = response;
    if (options.notifyOnFailed) {
      notification.config({
        duration: 4,
        maxCount: 2,
      });
      notification.error({
        message: `Request error ${status}`,
        description: errorText,
      });
    }
  }
};

export default successHandler;
