# upgrades to make:

1. getData.py
	package all data retrieval into a single Python file, so that no other files need to access binance. Call this getData.py
	This includes such helper methods as getMinTradeAmount(symbol) which only simplify code
2. MAIN LOOP
	Possible files to create: main.py
	Create a main.py file with a run-loop. Running this single file should run the entire system.
3. LOGGING SYSTEM: to keep track of everything that happens, for later reference
	Possible files to create: logger.py, storage.py, feedback.py
	See: https://docs.python.org/3/library/logging.html 

	This app's logging system should be capable of:
	a) 

	logging.py: should record events data, when trades/updates are made to the system **SESSIONS
	package all communications with terminal and with internal logs and csv files into one file. 
	No other files should need to read/write/print anything, unless through this comms_int.py file.
5. The system will have "levels". At the moment, we have only one, or two, levels: Logs and Rebalancing.
6. package the rebalancing system into Python script: rebalance.py, 
	which should handle building trade instructions off of passed data
7. Create a trade executer Python file, called trade.py. This package should be able to 