config = [
    {
        "subject":"NON-PROD Datafactory Pipeline Run Failed Alert",
        "template": "log-fail",
        "kql": "ADFActivityRun | where Status has 'Failed' | extend Subject = 'Workspace Alert' | extend ErrorProps=todynamic(Error) | project Subject, PipelineName,OperationName,ActivityName,TimeGenerated,ErrorProps['errorCode'],ErrorProps['message'],ErrorProps['failureType'],ErrorProps['target'],ErrorProps['details'] | order by TimeGenerated desc"
    },
    {
        "subject":"NON-PROD Datafactory Pipeline Run Success Alert",
        "template": "log-success",
        "kql": "ADFActivityRun | where Status == 'Succeeded' | extend ADF = strcat('https://adf.azure.com/en/home?factory=', _ResourceId) | project PipelineName,OperationName,ActivityName,TimeGenerated, ADF | order by TimeGenerated desc"
    }
]
