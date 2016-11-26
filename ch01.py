
import random

class Buffer:
    def __init__( self, max_wip, max_flow ):
        self.queued = 0
        self.wip = 0             # work-in-progress ("ready pool")

        self.max_wip = max_wip
        self.max_flow = max_flow # avg outflow is max_flow/2

    def work( self, u ):
        # Add to ready pool
        u = max( 0, int(round(u)) )
        u = min( u, self.max_wip )
        self.wip += u

        # Transfer from ready pool to queue
        r = int( round( random.uniform( 0, self.wip ) ) )   # randomly process some items from wip
        self.wip -= r
        self.queued += r

        # Release from queue to downstream process
        r = int( round( random.uniform( 0, self.max_flow ) ) )  # randomly process some items from queue
        r = min( r, self.queued )
        self.queued -= r

        return self.queued

class Controller:
    def __init__( self, kp, ki ):
        self.kp = kp    # proportional gain -> it is said proportional since it of the same magnitude of the current deviation
        self.ki = ki    # integral gain -> it prevents the control oscillating behaviour of the proportional gain itself
                        # avoiding to overshoot the correction

        self.i = 0       # Cumulative error ("integral")

    def work( self, e ):
        self.i += e     # cumulative sum of all deviations

        # the term (self.ki*self.i) will grow initially as we process items
        # after the initial big deviations in target error it will stabilize sufficiently

        return self.kp*e + self.ki*self.i   #released units = k p · error + k i · cumulative error

# ============================================================

def open_loop( p, tm=5000 ):
    def target( t ):
        return 5.0  # 5.1
    
    for t in range( tm ):
        u = target(t)
        y = p.work( u )

        print(t, u, 0, u, y)

def closed_loop( c, p, tm=5000 ):
    # this function basically defines the rules of the game
    # the setpoint defines how the systems behaves

    def setpoint( t ):
        if t < 100: return 0
        if t < 300: return 50
        return 10
    
    y = 0 
    for t in range( tm ):
        r = setpoint(t)

        # obviosly this can be NEGATIVE!
        e = r - y       # error: (target released items – actual queued items)
        u = c.work(e)
        y = p.work(u)   # simply apply transfers

        print(t, r, e, u, y)

# ============================================================

c = Controller( 1.25, 0.01 )
p = Buffer( 50, 10 )

# open_loop( p, 1000 ) # to test the Buffer itself
closed_loop( c, p, 1000 )