import logging
import ConfigParser


class App():
    """Application Framework:
    Depend:
        xxxx.conf:
            [name]
            log=xxxxx.log
    """
    logger = None

    def __init__(self, conf,
                 level=logging.INFO,
                 format='%(asctime)s %(levelname)s %(message)s',
                 name="DEFAULT"):
        """conf example:
            conf = 'deduct.conf'  --> ./deduct.conf --> /etc/deduct.conf
        """
        self.is_debug = False
        self.cfg = None
        self.config = None
        self.log_file = "/tmp/" + name + ".log"
        self.log_level = level
        self.format = format
        self.log_in_console = False

        self.config = ConfigParser.ConfigParser()
        if len(self.config.read(conf)) == 0:
            self.config.read("/etc/" + conf)
            print "load /etc/" + conf
        else:
            print "load ", conf

        try:
            cfg = dict(self.config.items(name))
            if "log" in cfg:
                self.log_file = cfg['log']
        except ConfigParser.NoSectionError:
            cfg = None
        print "log file:", self.log_file

    def debug(self, log):
        logger = self.get_logger()
        logger.debug(log)
        if self.is_debug and self.log_in_console:
            print log

    def info(self, log):
        logger = self.get_logger()
        logger.info(log)
        if self.log_in_console:
            print log

    def warning(self, log):
        logger = self.get_logger()
        logger.warning(log)
        if self.log_in_console:
            print log

    def error(self, log):
        logger = self.get_logger()
        logger.error(log)
        if self.log_in_console:
            print log

    def get_logger(self):
        if App.logger is None:
            App.logger = logging.getLogger()
            handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter(self.format)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(self.log_level)

        return App.logger

    def get_cfg(self, item):
        cfg = None

        try:
            cfg = dict(self.config.items(item))
        except ConfigParser.NoSectionError:
            pass

        return cfg
